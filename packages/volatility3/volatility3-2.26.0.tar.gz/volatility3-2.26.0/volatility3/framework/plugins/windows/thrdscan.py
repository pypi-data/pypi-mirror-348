##
## plugin for testing addition of threads scan support to poolscanner.py
##
import logging
import datetime
from typing import Callable, Iterable, Tuple, Optional, Dict

from volatility3.framework import renderers, interfaces, exceptions
from volatility3.framework.configuration import requirements
from volatility3.framework.renderers import format_hints
from volatility3.plugins.windows import poolscanner, pe_symbols
from volatility3.plugins import timeliner

vollog = logging.getLogger(__name__)


class ThrdScan(interfaces.plugins.PluginInterface, timeliner.TimeLinerInterface):
    """Scans for windows threads."""

    # version 2.6.0 adds support for scanning for 'Ethread' structures by pool tags
    _required_framework_version = (2, 6, 0)
    _version = (2, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.implementation = self.scan_threads

    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(
                name="kernel",
                description="Windows kernel",
                architectures=["Intel32", "Intel64"],
            ),
            requirements.VersionRequirement(
                name="poolscanner", component=poolscanner.PoolScanner, version=(3, 0, 0)
            ),
            requirements.VersionRequirement(
                name="pe_symbols", component=pe_symbols.PESymbols, version=(3, 0, 0)
            ),
            requirements.VersionRequirement(
                name="timeliner",
                component=timeliner.TimeLinerInterface,
                version=(1, 0, 0),
            ),
        ]

    @classmethod
    def scan_threads(
        cls,
        context: interfaces.context.ContextInterface,
        module_name: str,
    ) -> Iterable[interfaces.objects.ObjectInterface]:
        """Scans for threads using the poolscanner module and constraints.

        Args:
            context: The context to retrieve required elements (layers, symbol tables) from
            module_name: Name of the module to use for scanning

        Returns:
              A list of _ETHREAD objects found by scanning memory for the "Thre" / "Thr\\xE5" pool signatures
        """

        kernel = context.modules[module_name]

        constraints = poolscanner.PoolScanner.builtin_constraints(
            kernel.symbol_table_name, [b"Thr\xe5", b"Thre"]
        )

        for result in poolscanner.PoolScanner.generate_pool_scan(
            context, module_name, constraints
        ):
            _constraint, mem_object, _header = result
            yield mem_object

    @classmethod
    def gather_thread_info(
        cls,
        ethread: interfaces.objects.ObjectInterface,
        vads_cache: Dict[int, pe_symbols.ranges_type] = None,
    ) -> Tuple[
        int,
        int,
        int,
        int,
        Optional[str],
        int,
        Optional[str],
        Optional[datetime.datetime],
        Optional[datetime.datetime],
    ]:
        try:
            thread_offset = ethread.vol.offset
            owner_proc_pid = ethread.Cid.UniqueProcess
            thread_tid = ethread.Cid.UniqueThread
            thread_start_addr = ethread.StartAddress
            thread_win32start_addr = ethread.Win32StartAddress
            thread_create_time = (
                ethread.get_create_time()
            )  # datetime.datetime object / volatility3.framework.renderers.UnparsableValue object
            thread_exit_time = (
                ethread.get_exit_time()
            )  # datetime.datetime object / volatility3.framework.renderers.UnparsableValue object

            owner_proc = None
            if vads_cache is not None:
                owner_proc = ethread.owning_process()
        except exceptions.InvalidAddressException:
            vollog.debug(f"Thread invalid address {ethread.vol.offset:#x}")
            return None

        # don't look for VADs in kernel threads, just let them get reported with empty paths
        if owner_proc_pid != 4 and vads_cache is not None:
            vads = pe_symbols.PESymbols.get_vads_for_process_cache(
                vads_cache, owner_proc
            )
        else:
            vads = None

        start_path = (
            pe_symbols.PESymbols.filepath_for_address(vads, thread_start_addr)
            if vads
            else None
        )
        win32start_path = (
            pe_symbols.PESymbols.filepath_for_address(vads, thread_win32start_addr)
            if vads
            else None
        )

        return (
            format_hints.Hex(thread_offset),
            owner_proc_pid,
            thread_tid,
            format_hints.Hex(thread_start_addr),
            start_path,
            format_hints.Hex(thread_win32start_addr),
            win32start_path,
            thread_create_time,
            thread_exit_time,
        )

    def _generator(self, filter_func: Callable):
        kernel_name = self.config["kernel"]

        vads_cache: Dict[int, pe_symbols.ranges_type] = {}

        for ethread in self.implementation(self.context, kernel_name):
            info = self.gather_thread_info(ethread, vads_cache)

            if info:
                (
                    offset,
                    pid,
                    tid,
                    start_addr,
                    start_path,
                    win32start_addr,
                    win32start_path,
                    create_time,
                    exit_time,
                ) = info
                yield 0, (
                    offset,
                    pid,
                    tid,
                    start_addr,
                    start_path or renderers.NotAvailableValue(),
                    win32start_addr,
                    win32start_path or renderers.NotAvailableValue(),
                    create_time,
                    exit_time,
                )

    def generate_timeline(self):
        filt_func = self.filter_func(self.config)

        for row in self._generator(filt_func):
            _depth, row_data = row
            row_dict = {}
            (
                row_dict["Offset"],
                row_dict["PID"],
                row_dict["TID"],
                row_dict["StartAddress"],
                row_dict["CreateTime"],
                row_dict["ExitTime"],
            ) = row_data

            # Skip threads with no creation time
            # - mainly system process threads
            if not isinstance(row_dict["CreateTime"], datetime.datetime):
                continue
            description = f"Thread: Tid {row_dict['TID']} in Pid {row_dict['PID']} (Offset {row_dict['Offset']})"

            # yield created time, and if there is exit time, yield it too.
            yield (description, timeliner.TimeLinerType.CREATED, row_dict["CreateTime"])
            if isinstance(row_dict["ExitTime"], datetime.datetime):
                yield (
                    description,
                    timeliner.TimeLinerType.MODIFIED,
                    row_dict["ExitTime"],
                )

    @classmethod
    def filter_func(cls, config: interfaces.configuration.HierarchicalDict) -> Callable:
        """Returns a function that can filter this plugin's implementation method based on the config"""
        return lambda x: False

    def run(self):
        filt_func = self.filter_func(self.config)

        return renderers.TreeGrid(
            [
                ("Offset", format_hints.Hex),
                ("PID", int),
                ("TID", int),
                ("StartAddress", format_hints.Hex),
                ("StartPath", str),
                ("Win32StartAddress", format_hints.Hex),
                ("Win32StartPath", str),
                ("CreateTime", datetime.datetime),
                ("ExitTime", datetime.datetime),
            ],
            self._generator(filt_func),
        )

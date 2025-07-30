#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This module hooks IAT and EAT to monitor all external functions calls,
#    very useful for [malware] reverse and debugging.
#    Copyright (C) 2025  Win32Hooking

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This module hooks IAT and EAT to monitor all external functions calls,
very useful for [malware] reverse and debugging.
"""

__version__ = "1.1.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This module hooks IAT and EAT to monitor all external functions calls,
very useful for [malware] reverse and debugging.
"""
__url__ = "https://github.com/mauricelambert/Win32Hooking"

# __all__ = []

__license__ = "GPL-3.0 License"
__copyright__ = """
Win32Hooking  Copyright (C) 2025  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

from ctypes import (
    windll,
    WinError,
    Structure,
    CFUNCTYPE,
    POINTER,
    memmove,
    cast,
    byref,
    addressof,
    sizeof,
    get_last_error,
    string_at,
    c_size_t,
    c_void_p,
    c_byte,
    c_char,
    c_int,
    c_uint8,
    c_uint16,
    c_ushort,
    c_uint32,
    c_ulong,
    c_uint64,
    c_ulonglong,
    c_char_p,
    c_wchar_p,
)
from PyPeLoader import (
    IMAGE_DOS_HEADER,
    IMAGE_NT_HEADERS,
    IMAGE_FILE_HEADER,
    IMAGE_OPTIONAL_HEADER64,
    IMAGE_OPTIONAL_HEADER32,
    ImportFunction,
    PeHeaders,
    load_headers,
    load_in_memory,
    get_imports,
    load_relocations,
)
from ctypes.wintypes import (
    DWORD,
    HMODULE,
    MAX_PATH,
    HANDLE,
    BOOL,
    LPCWSTR,
    LPVOID,
)
from typing import Iterator, Callable, Dict, Union, List, Tuple
from logging import StreamHandler, DEBUG, FileHandler, Logger
from PythonToolsKit.Logs import get_custom_logger
from sys import argv, executable, exit, stderr
from threading import get_native_id, Lock
from dataclasses import dataclass, field
from os.path import basename, splitext
from json import load as json_load
from _io import _BufferedIOBase
from re import fullmatch
from os import getpid

PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_READ = 0x20
PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_FREE = 0x10000

IMAGE_DIRECTORY_ENTRY_EXPORT = 0
TH32CS_SNAPMODULE = 0x00000008


class CallbackManager:
    lock: Lock = Lock()
    thread_id: int = 0
    indent: int = 0
    config: dict = {}
    run: bool = -1


class UNICODE_STRING(Structure):
    """
    This class implements the Unicode String for
    LdrLoadDll argument value.
    """

    _fields_ = [
        ("Length", c_ushort),
        ("MaximumLength", c_ushort),
        ("Buffer", c_wchar_p),
    ]


class MODULEENTRY32(Structure):
    """
    This class implements the Module Entry for
    CreateToolhelp32Snapshot return value.
    """

    _fields_ = [
        ("dwSize", DWORD),
        ("th32ModuleID", DWORD),
        ("th32ProcessID", DWORD),
        ("GlblcntUsage", DWORD),
        ("ProccntUsage", DWORD),
        ("modBaseAddr", POINTER(c_byte)),
        ("modBaseSize", DWORD),
        ("hModule", HMODULE),
        ("szModule", c_char * 256),
        ("szExePath", c_char * MAX_PATH),
    ]


class IMAGE_EXPORT_DIRECTORY(Structure):
    """
    This class implements the image export directory
    to access export functions.
    """

    _fields_ = [
        ("Characteristics", c_uint32),
        ("TimeDateStamp", c_uint32),
        ("MajorVersion", c_uint16),
        ("MinorVersion", c_uint16),
        ("Name", c_uint32),
        ("Base", c_uint32),
        ("NumberOfFunctions", c_uint32),
        ("NumberOfNames", c_uint32),
        ("AddressOfFunctions", c_uint32),  # RVA to DWORD array
        ("AddressOfNames", c_uint32),  # RVA to RVA array (function names)
        ("AddressOfNameOrdinals", c_uint32),  # RVA to WORD array
    ]


class MEMORY_BASIC_INFORMATION(Structure):
    """
    This class implements the structure to get memory information.
    """

    _fields_ = [
        ("BaseAddress", c_void_p),
        ("AllocationBase", c_void_p),
        ("AllocationProtect", DWORD),
        ("RegionSize", c_size_t),
        ("State", DWORD),
        ("Protect", DWORD),
        ("Type", DWORD),
    ]


X86_CONTEXT_i386 = 0x00010000
X86_CONTEXT_CONTROL = 0x00000001
X86_CONTEXT_INTEGER = 0x00000002
X86_CONTEXT_FULL = X86_CONTEXT_CONTROL | X86_CONTEXT_INTEGER | X86_CONTEXT_i386


class FLOATING_SAVE_AREA(Structure):
    _fields_ = [
        ("ControlWord", c_uint32),
        ("StatusWord", c_uint32),
        ("TagWord", c_uint32),
        ("ErrorOffset", c_uint32),
        ("ErrorSelector", c_uint32),
        ("DataOffset", c_uint32),
        ("DataSelector", c_uint32),
        ("RegisterArea", c_byte * 80),
        ("Cr0NpxState", c_uint32),
    ]


class CONTEXT32(Structure):
    _fields_ = [
        ("ContextFlags", c_uint32),
        ("Dr0", c_uint32),
        ("Dr1", c_uint32),
        ("Dr2", c_uint32),
        ("Dr3", c_uint32),
        ("Dr6", c_uint32),
        ("Dr7", c_uint32),
        ("FloatSave", FLOATING_SAVE_AREA),
        ("SegGs", c_uint32),
        ("SegFs", c_uint32),
        ("SegEs", c_uint32),
        ("SegDs", c_uint32),
        ("Edi", c_uint32),
        ("Esi", c_uint32),
        ("Ebx", c_uint32),
        ("Edx", c_uint32),
        ("Ecx", c_uint32),
        ("Eax", c_uint32),
        ("Ebp", c_uint32),
        ("Eip", c_uint32),
        ("SegCs", c_uint32),
        ("EFlags", c_uint32),
        ("Esp", c_uint32),
        ("SegSs", c_uint32),
        ("ExtendedRegisters", c_byte * 512),
    ]


X64_CONTEXT_CONTROL = 0x00100001
X64_CONTEXT_INTEGER = 0x00010000
X64_CONTEXT_FULL = X64_CONTEXT_CONTROL | X64_CONTEXT_INTEGER

is_x64: bool = sizeof(c_void_p) == 8


class CONTEXT64(Structure):
    """
    This class is the ThreadContext structure for NtCreateThread.
    """

    _fields_ = [
        ("P1Home", c_ulonglong),
        ("P2Home", c_ulonglong),
        ("P3Home", c_ulonglong),
        ("P4Home", c_ulonglong),
        ("P5Home", c_ulonglong),
        ("P6Home", c_ulonglong),
        ("ContextFlags", c_ulong),
        ("MxCsr", c_ulong),
        ("SegCs", c_ushort),
        ("SegDs", c_ushort),
        ("SegEs", c_ushort),
        ("SegFs", c_ushort),
        ("SegGs", c_ushort),
        ("SegSs", c_ushort),
        ("EFlags", c_ulong),
        ("Dr0", c_ulonglong),
        ("Dr1", c_ulonglong),
        ("Dr2", c_ulonglong),
        ("Dr3", c_ulonglong),
        ("Dr6", c_ulonglong),
        ("Dr7", c_ulonglong),
        ("Rax", c_ulonglong),
        ("Rcx", c_ulonglong),
        ("Rdx", c_ulonglong),
        ("Rbx", c_ulonglong),
        ("Rsp", c_ulonglong),
        ("Rbp", c_ulonglong),
        ("Rsi", c_ulonglong),
        ("Rdi", c_ulonglong),
        ("R8", c_ulonglong),
        ("R9", c_ulonglong),
        ("R10", c_ulonglong),
        ("R11", c_ulonglong),
        ("R12", c_ulonglong),
        ("R13", c_ulonglong),
        ("R14", c_ulonglong),
        ("R15", c_ulonglong),
        ("Rip", c_ulonglong),
    ]


@dataclass
class Function:
    module: MODULEENTRY32
    module_name: str
    name: str
    address: int
    rva: int
    export_address: int
    index: int
    pointer: type = None
    hook: Callable = None
    arguments: List[str] = None
    hide: bool = False
    count_call: int = 0
    calls: List[Dict[str, Union[int, Callable]]] = field(default_factory=list)


class Callbacks:
    """
    This class contains all callbacks define in configuration.
    """

    def ntdll_NtCreateThreadEx_pre(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
    ) -> Tuple:
        """
        This function is a callback executed before the NtCreateThreadEx
        execution to change the start address to initialize the new stack.
        """

        arguments = (
            arguments[0],
            arguments[1],
            arguments[2],
            arguments[3],
            get_thread_hook(arguments[4]),
            arguments[5],
            arguments[6],
            arguments[7],
            arguments[8],
            arguments[9],
            arguments[10],
        )

        callback_print(
            "               ",
            "call  ",
            function.module_name,
            function.name + ":",
            *(
                [
                    (
                        f"{x} = {arguments[i]} ({arguments[i]:x})"
                        if isinstance(arguments[i], int)
                        else f"{x} = {arguments[i]}"
                    )
                    for i, x in enumerate(function.arguments)
                ]
                if function.arguments
                else []
            ),
        )

        return arguments

    def ntdll_NtCreateThread_pre(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
    ) -> Tuple:
        """
        This function is a callback executed before the NtCreateThread
        execution to change the start address to initialize the new stack.
        """

        if is_x64:
            context = CONTEXT64()
            size = sizeof(CONTEXT64)
        else:
            context = CONTEXT32()
            size = sizeof(CONTEXT32)

        memmove(addressof(context), arguments[5], size)

        if is_x64:
            context.Rip = get_thread_hook(context.Rip)
        else:
            context.Eip = new_ip

        memmove(arguments[5], addressof(context), size)
        return arguments

    def breakpoint(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function is a simple breakpoint to block the execution and analyze
        arguments and returns values.
        """

        breakpoint()

    def kernelbase_GetWindowsDirectoryW(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the GetWindowsDirectoryW hooking behavior.
        """

        if return_value:
            print(
                " " * (4 * (CallbackManager.indent + 1)),
                "GetWindowsDirectoryW: [OUT] Path =",
                c_wchar_p(arguments[0]).value + ",",
                "[IN] Size =",
                arguments[1],
                "[OUT] Number of bytes written =",
                return_value,
            )
        return return_value

    def kernelbase_GetModuleHandleExW(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the GetModuleHandleExW hooking behavior.
        """

        if arguments[0] != 4:
            print(
                " " * (4 * (CallbackManager.indent + 1)),
                "GetModuleHandleExW:",
                "[IN] Flags =",
                hex(arguments[0]) + ",",
                "[IN] Module Name =",
                c_wchar_p(arguments[1]).value,
                "[OUT] Module Handle =",
                hex(arguments[2] if arguments[2] else 0) + ",",
                "[OUT] Success =",
                bool(return_value),
            )

        return return_value

    def kernelbase_GetModuleFileNameW(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the GetModuleFileNameW hooking behavior.
        """

        if return_value:
            print(
                " " * (4 * (CallbackManager.indent + 1)),
                "GetModuleFileNameW:",
                "[IN] Module Handle =",
                hex(arguments[0] if arguments[0] else 0) + ",",
                "[OUT] Filename =",
                c_wchar_p(arguments[1]).value,
                "[IN] Size =",
                str(arguments[2]) + ",",
                "[OUT] Number of bytes written =",
                return_value,
            )

        return return_value

    def ntdll_ApiSetQueryApiSetPresence(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the ApiSetQueryApiSetPresence hooking behavior.
        """

        namespace = cast(arguments[0], POINTER(UNICODE_STRING)).contents
        present = cast(arguments[1], POINTER(c_bool)).contents.value

        print(
            " " * (4 * (CallbackManager.indent + 1)),
            "ApiSetQueryApiSetPresence: [IN] Namespace =",
            repr(unicode_string.Buffer) + ",",
            "[OUT] Present =",
            str(present) + ',',
            '[OUT] Return =',
            str(return_value)
        )

        return return_value

    def ntdll_LdrLoadDll(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the LdrLoadDll hooking behavior.
        """

        unicode_string = cast(arguments[2], POINTER(UNICODE_STRING)).contents
        module_handle = cast(arguments[3], POINTER(c_uint64)).contents.value

        dos_headers = cast(module_handle, POINTER(IMAGE_DOS_HEADER)).contents
        nt_position = module_handle + dos_headers.e_lfanew
        nt_headers = cast(nt_position, POINTER(IMAGE_NT_HEADERS)).contents
        file_header = nt_headers.FileHeader

        if file_header.Machine == 0x014C:  # IMAGE_FILE_MACHINE_I386
            optional_header = nt_headers.OptionalHeader
            arch = 32
        elif file_header.Machine == 0x8664:  # IMAGE_FILE_MACHINE_AMD64
            optional_header_position = (
                nt_position
                + sizeof(IMAGE_NT_HEADERS)
                - sizeof(IMAGE_OPTIONAL_HEADER32)
            )
            optional_header = cast(
                optional_header_position, POINTER(IMAGE_OPTIONAL_HEADER64)
            ).contents
            arch = 64

        module = MODULEENTRY32(
            sizeof(MODULEENTRY32),
            1,
            getpid(),
            0,
            1,
            cast(module_handle, POINTER(c_byte)),
            optional_header.SizeOfImage,
            module_handle,
            unicode_string.Buffer.encode("latin-1").ljust(256, b"\0"),
            b"\0" * MAX_PATH,
        )

        if module_handle not in modules:
            imports = []
            hooks_DLL(module, Hooks.export_hooks, imports)
            hooks_IAT(imports, False)

        print(
            " " * (4 * (CallbackManager.indent + 1)),
            "LdrLoadDll: [IN] Path =",
            str(c_wchar_p(arguments[0])) + ",",
            "[IN] Flags =",
            hex(cast(arguments[1], POINTER(c_ulong)).contents.value) + ",",
            "[IN] Module =",
            repr(unicode_string.Buffer) + ",",
            "[OUT] Handle =",
            module_handle,
            "(" + hex(module_handle) + ")",
        )
        return return_value

    def kernel32_GetProcAddress(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines the GetProcAddress hooking behavior.
        """

        module = arguments[0]
        function_name = arguments[1].decode()
        identifier = str(module) + "|" + function_name

        if (proc := Hooks.get_proc_address_hooks.get(identifier)) is None:
            func = Hooks.export_hooks[identifier]
            proc = Function(
                func.module,
                func.module_name,
                func.name,
                func.address,
                func.rva,
                func.export_address,
                func.index,
            )
            build_generic_callback("GetProcAddress", proc)
            Hooks.get_proc_address_hooks[identifier] = proc

        proc_pointer = cast(proc.hook, c_void_p).value
        callback_print(
            (" " * (4 * (CallbackManager.indent + 1)))
            + f"GetProcAddress: Module = {hex(module)} ({proc.module_name})"
            f", Function = {function_name}, HookAddress = {hex(proc_pointer)}"
        )

        logger.info(
            "Hook "
            + proc.module_name
            + " "
            + proc.name
            + " "
            + hex(proc.address)
            + " "
            + hex(proc_pointer)
            + " "
            + hex(proc.rva)
        )

        return proc_pointer

    def interactive(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function defines interactive actions on callback.
        """

        # answer = None
        # while answer not in ("b", "c", "e"):
        #     answer = input(
        #         "Enter [b] for breakpoint, [c] to continue and [e] to exit: "
        #     )

        # if answer == "b":
        #     breakpoint()
        # elif answer == "e":
        #     exit(1)

        return return_value

    def exit(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function terminates/exits the program.
        """

        function_type = CFUNCTYPE(c_void_p, c_int)
        function = function_type(
            Hooks.name_hooks["KERNEL32.DLL|ExitProcess"].address
        )
        return function(0)

    def print(
        type_: str,
        function: Union[Function, ImportFunction],
        arguments: Tuple,
        return_value: c_void_p,
    ) -> c_void_p:
        """
        This function prints function, return value and arguments,
        it's a simple demo.
        """

        print(type_, function.module, function.name, arguments, return_value)
        return return_value


class Hooks:
    """
    This class contains all data about hooks.
    """

    get_proc_address_hooks: Dict[str, Function] = {}
    reserved_hooks_space: Dict[str, int] = {}
    export_hooks: Dict[str, Function] = {}
    import_hooks: Dict[str, ImportFunction] = {}
    name_hooks: Dict[str, Function] = {}
    types: Dict[str, CFUNCTYPE] = {}
    threads_stack_alloc: Dict[int, int] = {}


def resolve_type(module_type: str) -> type:
    """
    This function returns a type from python module.
    """

    modules, type_ = module_type.rsplit(".", 1)
    module = __import__(modules)
    for element in modules.split(".")[1:]:
        module = getattr(module, element)
    return getattr(module, type_)


def get_callback_type(
    arguments: Union[None, List[Dict[str, str]]],
    return_value: Union[str, None],
) -> CFUNCTYPE:
    """
    This function builds and returns the callback CFUNCTYPE.
    """

    if arguments is None and return_value is None:
        return generic_callback

    if return_value is None:
        return_value = c_void_p
    else:
        return_value = resolve_type(return_value)

    if arguments is None:
        arguments_ = [c_void_p] * 67
    else:
        arguments_ = []
        for argument in arguments:
            arguments_.append(resolve_type(argument["type"]))

    return CFUNCTYPE(return_value, *arguments_)


generic_callback = CFUNCTYPE(c_void_p, *([c_void_p] * 67))

kernel32 = windll.kernel32

CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]
CreateToolhelp32Snapshot.restype = HANDLE

Module32First = kernel32.Module32First
Module32First.argtypes = [HANDLE, POINTER(MODULEENTRY32)]
Module32First.restype = BOOL

Module32Next = kernel32.Module32Next
Module32Next.argtypes = [HANDLE, POINTER(MODULEENTRY32)]
Module32Next.restype = BOOL

CloseHandle = kernel32.CloseHandle

VirtualProtect = kernel32.VirtualProtect
VirtualProtect.argtypes = [c_void_p, c_size_t, DWORD, POINTER(DWORD)]
VirtualProtect.restype = BOOL

VirtualAlloc = kernel32.VirtualAlloc
VirtualAlloc.argtypes = [c_void_p, c_size_t, DWORD, DWORD]
VirtualAlloc.restype = LPVOID

GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandleW.restype = HMODULE

LoadLibraryW = kernel32.LoadLibraryW
LoadLibraryW.argtypes = [LPCWSTR]
LoadLibraryW.restype = HMODULE

GetProcAddress = kernel32.GetProcAddress
GetProcAddress.argtypes = [HMODULE, c_char_p]
GetProcAddress.restype = c_void_p

modules: Dict[Union[int, str], MODULEENTRY32] = {}


def get_logger(name: str) -> Logger:
    """
    This function gets a specific logger and modify
    the handler but keep the formatter.
    """

    logger = get_custom_logger(name)
    file_handler = FileHandler(name + ".log")
    logger.addHandler(file_handler)
    logger.setLevel(DEBUG)

    for handler in logger.handlers:
        if isinstance(handler, StreamHandler):
            file_handler.setFormatter(handler.formatter)
            logger.removeHandler(handler)

    return logger


logger = get_logger(splitext(basename(__file__))[0])
callback_logger = get_logger("callback")


def init_lock() -> bool:
    """
    This function manages concurrency for callbacks.
    """

    thread_id = get_native_id()
    acquire = thread_id != CallbackManager.thread_id
    if acquire:
        CallbackManager.lock.acquire()
        CallbackManager.thread_id = thread_id

    return acquire


def reset_lock(acquire: bool) -> None:
    """
    This function releases locker and resets elements for concurrency.
    """

    if acquire:
        CallbackManager.indent = 0
        CallbackManager.thread_id = None
        CallbackManager.lock.release()
    else:
        CallbackManager.indent -= 1


def callback_print(*args, **kwargs) -> None:
    """
    This function manages callbacks prints.
    """

    separator = kwargs.get("sep", " ")
    to_print = separator.join(args)
    print(to_print, **kwargs)
    callback_logger.info(to_print)


def callback_call_printer(
    function: ImportFunction,
    callback_type: Callable,
    arguments: Tuple,
    start: str,
) -> None:
    """
    This function prints call for not hidden callback.
    """

    if function.hide:
        return None

    CallbackManager.indent += 1
    if isinstance(function, ImportFunction):
        module = function.module_name + " (" + function.module_container + ")"
    else:
        module = function.module_name
    if callback_type is generic_callback:
        callback_print(start, "call  ", module, function.name)
    else:
        callback_print(
            start,
            "call  ",
            module,
            function.name + ":",
            *(
                [
                    (
                        f"{x} = {arguments[i]} ({arguments[i]:x})"
                        if isinstance(arguments[i], int)
                        else f"{x} = {arguments[i]}"
                    )
                    for i, x in enumerate(function.arguments)
                ]
                if function.arguments
                else []
            ),
        )


def callback_return_printer(
    function: ImportFunction, return_value: c_void_p, start: str
) -> None:
    """
    This function prints return for not hidden callback.
    """

    if function.hide:
        return None

    callback_print(
        start,
        "return",
        function.module_name,
        function.name + ":",
        (
            (str(return_value) + " (" + hex(return_value) + ")")
            if return_value is not None and not isinstance(return_value, str)
            else str(return_value)
        ),
    )


def callback_call(
    function: ImportFunction,
    specific_call: Callable,
    return_value: c_void_p,
    type_: str,
    arguments: Tuple,
) -> c_void_p:
    """
    This function detects which callback should be call and call it.
    """

    temp_specific_call = None

    if len(function.calls) > function.count_call:
        call = function.calls[function.count_call]
        return_value = call.get("return_value", return_value)
        temp_specific_call = call.get("post_callback", specific_call)

    if temp_specific_call := (temp_specific_call or specific_call):
        return_value = temp_specific_call(
            type_, function, arguments, return_value
        )

    return return_value


def pre_callback_call(
    function: ImportFunction,
    type_: str,
    arguments: Tuple,
) -> Tuple:
    """
    This function detects which callback should be call and call it.
    """

    temp_specific_call = None

    if len(function.calls) > function.count_call:
        temp_specific_call = function.calls[function.count_call].get(
            "pre_callback", function.pre_exec_hook
        )

    if temp_specific_call := (temp_specific_call or function.pre_exec_hook):
        arguments = temp_specific_call(type_, function, arguments)

    return arguments


def generic_callback_generator(
    type_: str,
    function: Union[Function, ImportFunction],
    specific_call: Callable = None,
    callback_type: CFUNCTYPE = generic_callback,
) -> Callable:
    """
    This function makes the specific callback for each function
    using the generic callback.
    """

    @callback_type
    def callback(*arguments):
        if CallbackManager.run != get_native_id():
            return function.pointer(*arguments)

        acquire = init_lock()
        CallbackManager.run = -1
        start = ((CallbackManager.indent * 4) * " ") + type_
        callback_call_printer(function, callback_type, arguments, start)
        arguments = pre_callback_call(function, type_, arguments)

        function_pointer = callback_type(function.address)
        CallbackManager.run = get_native_id()
        return_value = function_pointer(*arguments)
        CallbackManager.run = -1

        return_value = callback_call(
            function, specific_call, return_value, type_, arguments
        )
        function.count_call += 1
        callback_return_printer(function, return_value, start)

        CallbackManager.run = get_native_id()
        reset_lock(acquire)
        return return_value

    return callback


def find_free_executable_region(
    start_address: int, function_number: int, max_scan=0x10000000
) -> int:
    """
    This function implements checks on memory to get a good address to
    allocate hooks jumps.
    """

    mbi = MEMORY_BASIC_INFORMATION()
    size_needed = function_number * 12
    current = start_address
    step = 0x100000

    while current < start_address + max_scan:
        result = kernel32.VirtualQuery(
            c_void_p(current), byref(mbi), sizeof(mbi)
        )

        if result == 0:
            break

        if mbi.State == MEM_FREE:
            alloc = kernel32.VirtualAlloc(
                c_void_p(current),
                c_size_t(size_needed),
                MEM_RESERVE | MEM_COMMIT,
                PAGE_EXECUTE_READ,
            )

            if alloc:
                return alloc

        current += step

    return 0


def generate_absolute_jump(address: int) -> bytes:
    """
    This function generates an absolute JUMP instruction.
    """

    mov_rax = b"\x48\xb8" + address.to_bytes(8, byteorder="little")
    jmp_rax = b"\xff\xe0"
    return mov_rax + jmp_rax

def generate_absolute_call(address: int) -> bytes:
    """
    This function generates an absolute CALL instruction.
    """
    mov_rax = b"\x48\xb8" + address.to_bytes(8, byteorder="little")
    call_rax = b"\xff\xd0"
    return mov_rax + call_rax

def build_stack_debug_shellcode(printf_addr: int) -> bytes:
    """
    Build position-independent x64 shellcode that:
      - Computes RBP - RSP (used stack in current function)
      - Calls printf("Stack used: 0x%llx\n", <usage>)
    """
    shellcode = b""

    # sub rsp, 0x28  ; align + shadow space (Win x64 ABI)
    shellcode += b"\x48\x83\xEC\x28"

    # mov rax, rbp
    shellcode += b"\x48\x89\xE8"

    # sub rax, rsp  ; rax = rbp - rsp
    shellcode += b"\x48\x29\xE0"

    # lea rcx, [rip+0] ; will be patched to point to format string
    shellcode += b"\x48\x8D\x0D\x00\x00\x00\x00"

    # mov rdx, rax
    shellcode += b"\x48\x89\xC2"

    # mov rax, <printf_addr>
    printf_bytes = c_uint64(printf_addr)
    printf_raw = string_at(byref(printf_bytes), 8)
    shellcode += b"\x48\xB8" + printf_raw

    # call rax
    shellcode += b"\xFF\xD0"

    # add rsp, 0x28
    shellcode += b"\x48\x83\xC4\x28"

    # format string: "Stack used: 0x%llx\n\0"
    fmt = b"Stack used: 0x%llx\n\0"
    offset = len(shellcode)
    shellcode += fmt

    # Patch LEA offset (relative to next instruction after lea)
    rel_offset = offset - (10 + 7)
    offset_bytes = string_at(byref(c_uint32(rel_offset)), 4)
    shellcode = shellcode[:13] + offset_bytes + shellcode[17:]

    return shellcode


def generate_new_thread_stack(address: int) -> bytes:
    """
    This function generates the stack for the new thread.
    """

    shellcode = b''

    for key, function in Hooks.name_hooks.items():
        if key == "MSVCRT.DLL|printf":
            shellcode = build_stack_debug_shellcode(function.address)

    return (
        b"\x48\x81\xec\x00\x02\x00\x00"                    # sub rsp, 0x200
        + shellcode
        + generate_absolute_call(address)
        + b"\x48\x81\xc4\x00\x02\x00\x00\x48\x31\xc0\xc3"  # add rsp, 0x200
                                                           # xor rax, rax
                                                           # ret
    )


def executable_instructions(instructions: bytes) -> int:
    """
    Allocate memory, write data to it, change the permissions to read-execute,
    and return the address.
    """

    size = len(instructions)
    allocated_memory = VirtualAlloc(
        None, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE
    )

    if not allocated_memory:
        raise MemoryError("Failed to allocate memory.")

    memmove(allocated_memory, instructions, size)

    old_protect = DWORD()
    result = VirtualProtect(
        allocated_memory, size, PAGE_EXECUTE_READ, byref(old_protect)
    )

    if not result:
        raise MemoryError("Failed to change memory protection.")

    return allocated_memory


def get_thread_hook(start_address: int):
    '''
    This function returns the thread hooks for a specific starting point.
    '''

    if Hooks.threads_stack_alloc.get(start_address):
        thread_hook = start_address
    else:
        thread_hook = executable_instructions(
            generate_new_thread_stack(start_address)
        )
        Hooks.threads_stack_alloc[thread_hook] = start_address

    return thread_hook

def write_in_memory(address: int, data: bytes) -> None:
    """
    This function writes data at specified memory with permissions management.
    """

    size = len(data)
    old_protect = DWORD()

    if not VirtualProtect(address, size, PAGE_READWRITE, byref(old_protect)):
        raise WinError()

    memmove(address, c_char_p(data), size)

    if not VirtualProtect(address, size, old_protect.value, byref(DWORD())):
        raise WinError()


def build_generic_callback(type_: str, function: Function) -> None:
    """
    This function builds the generic callback using configurations.
    """

    def get_callback(config, type_):
        if callback := config.get(type_):
            if not isinstance(callback, Callable):
                return getattr(Callbacks, config[type_])
            return config[type_]

    identifier = (
        function.module_name.upper() + "|" + function.name
        if isinstance(function.name, str)
        else ("*" + str(function.name))
    )
    function_config = CallbackManager.config["functions"].get(
        identifier,
        CallbackManager.config["default"],
    )
    arguments = function_config.get("arguments")

    callback_type = Hooks.types.get(identifier) or get_callback_type(
        arguments, function_config.get("return_value")
    )
    Hooks.types[identifier] = callback_type
    function.pointer = callback_type(function.address)

    function.hook = generic_callback_generator(
        type_,
        function,
        get_callback(function_config, "post_callback"),
        callback_type,
    )
    function.pre_exec_hook = get_callback(function_config, "pre_callback")
    function.arguments = arguments and [x["name"] for x in arguments]
    function.hide = function_config.get("hide", False)

    calls = []
    for call in function_config.get("calls", []):
        call["post_callback"] = get_callback(call, "post_callback")
        calls.append(call)
    function.calls = calls


def hook_function(function: Function) -> None:
    """
    This function hooks the function send as argument.
    """

    logger.info("Hook " + function.module_name + " " + function.name)
    module_base = addressof(function.module.modBaseAddr.contents)
    real_value = cast(
        function.export_address, POINTER(c_uint32)
    ).contents.value

    if (
        hook_jump_address := Hooks.reserved_hooks_space.get(
            function.module_name
        )
    ) is None:
        hook_jump_address = find_free_executable_region(
            module_base + function.module.modBaseSize,
            function.module.export_directory.NumberOfFunctions,
        )
        Hooks.reserved_hooks_space[function.module_name] = hook_jump_address

    build_generic_callback("EAT", function)

    hook_pointer = cast(function.hook, c_void_p).value
    jump_instructions = generate_absolute_jump(hook_pointer)

    hook_jump_address += 12 * function.index
    hook_rva = hook_jump_address - module_base

    write_in_memory(
        function.export_address, hook_rva.to_bytes(4, byteorder="little")
    )
    write_in_memory(hook_jump_address, jump_instructions)
    hook_value = cast(
        function.export_address, POINTER(c_uint32)
    ).contents.value
    resolved_address = kernel32.GetProcAddress(
        module_base, function.name.encode()
    )

    logger.info(
        "Hook "
        + function.module_name
        + " "
        + function.name
        + " "
        + hex(real_value)
        + " "
        + hex(hook_value)
        + " "
        + hex(hook_rva)
        + " "
        + hex(hook_jump_address)
        + " "
        + hex(resolved_address)
    )


def rva_to_addr(base: int, rva: int) -> POINTER:
    """
    This function returns a pointer from a RVA.
    """

    return cast(base + rva, POINTER(c_uint8))


def rva_to_struct(base: int, rva: int, struct_type: Structure) -> Structure:
    """
    This function returns the structure instance from RVA.
    """

    return cast(base + rva, POINTER(struct_type)).contents


def load_headers_from_memory(
    module: MODULEENTRY32,
) -> Tuple[
    int,
    IMAGE_DOS_HEADER,
    IMAGE_NT_HEADERS,
    Union[IMAGE_OPTIONAL_HEADER64, IMAGE_OPTIONAL_HEADER32],
]:
    """
    This function returns all headers and inforamtions about the
    module (DLL) loaded in memory.
    """

    module_base = addressof(module.modBaseAddr.contents)
    dos = cast(module_base, POINTER(IMAGE_DOS_HEADER)).contents

    if dos.e_magic != 0x5A4D:
        raise ValueError("Invalid DOS header magic")

    nt_headers_address = module_base + dos.e_lfanew
    nt_headers = cast(nt_headers_address, POINTER(IMAGE_NT_HEADERS)).contents

    if nt_headers.Signature != 0x00004550:
        raise ValueError("Invalid PE signature")

    if nt_headers.FileHeader.Machine == 0x014C:
        optional_header = nt_headers.OptionalHeader
    elif nt_headers.FileHeader.Machine == 0x8664:
        optional_header = cast(
            nt_headers_address + 4 + sizeof(IMAGE_FILE_HEADER),
            POINTER(IMAGE_OPTIONAL_HEADER64),
        ).contents
    else:
        raise ValueError("Invalid Machine value NT File Headers")

    return module_base, dos, nt_headers, optional_header


def get_PeHeaders(
    module_base: int,
    dos: IMAGE_DOS_HEADER,
    nt_headers: IMAGE_NT_HEADERS,
    optional_header: Union[IMAGE_OPTIONAL_HEADER64, IMAGE_OPTIONAL_HEADER32],
) -> PeHeaders:
    """
    This function returns the PeHeaders to call PyPeLoader.get_imports
    """

    return PeHeaders(
        dos,
        nt_headers,
        nt_headers.FileHeader,
        optional_header,
        None,
        64 if isinstance(optional_header, IMAGE_OPTIONAL_HEADER64) else 32,
    )


def list_exports(
    module: MODULEENTRY32,
    module_base: int,
    dos: IMAGE_DOS_HEADER,
    nt_headers: IMAGE_NT_HEADERS,
    optional_header: Union[IMAGE_OPTIONAL_HEADER64, IMAGE_OPTIONAL_HEADER32],
) -> Iterator[Function]:
    """
    This function returns exported functions.
    """

    export_directory = optional_header.DataDirectory[
        IMAGE_DIRECTORY_ENTRY_EXPORT
    ]
    module.export_directory_rva = export_dirrectory_rva = (
        export_directory.VirtualAddress
    )
    module.export_directory_size = export_directory.Size

    if export_dirrectory_rva == 0:
        return None

    module.export_directory = export_directory = rva_to_struct(
        module_base, export_dirrectory_rva, IMAGE_EXPORT_DIRECTORY
    )

    base_export_functions_addresses = (
        module_base + export_directory.AddressOfFunctions
    )
    addresses_of_names = cast(
        module_base + export_directory.AddressOfNames,
        POINTER(c_uint32 * export_directory.NumberOfNames),
    ).contents
    addresses_of_functions = cast(
        base_export_functions_addresses,
        POINTER(c_uint32 * export_directory.NumberOfFunctions),
    ).contents
    addresses_of_ordinals = cast(
        module_base + export_directory.AddressOfNameOrdinals,
        POINTER(c_uint16 * export_directory.NumberOfNames),
    ).contents

    for i in range(export_directory.NumberOfNames):
        name_rva = addresses_of_names[i]
        ordinal = addresses_of_ordinals[i]
        function_rva = addresses_of_functions[ordinal]

        name_ptr = cast(module_base + name_rva, c_char_p)
        function_addr = module_base + function_rva

        yield Function(
            module,
            module.szModule.decode(),
            name_ptr.value.decode(),
            function_addr,
            function_rva,
            base_export_functions_addresses + ordinal * 4,
            i,
        )


def list_modules() -> Iterator[MODULEENTRY32]:
    """
    This generator yields the base address for each module.
    """

    pid = getpid()
    handle_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)
    if handle_snapshot == HANDLE(-1).value:
        raise WinError(get_last_error())

    module_entry = MODULEENTRY32()
    module_entry.dwSize = sizeof(MODULEENTRY32)

    success = Module32First(handle_snapshot, byref(module_entry))
    if not success:
        CloseHandle(handle_snapshot)
        raise WinError(get_last_error())

    while success:
        base_addr = addressof(module_entry.modBaseAddr.contents)
        yield module_entry
        success = Module32Next(handle_snapshot, byref(module_entry))

    CloseHandle(handle_snapshot)


def hooks_DLL(
    module: MODULEENTRY32,
    functions: Dict[str, Function],
    imports: List[ImportFunction],
) -> List[Function]:
    """
    This function hooks a module function addresses
    (all functions in EAT and configured functions in IAT).
    """

    base_address = addressof(module.modBaseAddr.contents)
    headers = load_headers_from_memory(module)
    imports.extend(
        get_imports(
            get_PeHeaders(*headers), headers[0], module.szModule.decode()
        )
    )
    forwarded_functions = []

    new_module = MODULEENTRY32()
    memmove(byref(new_module), byref(module), sizeof(MODULEENTRY32))
    modules[base_address] = new_module
    modules[new_module.szModule] = new_module

    for function in list_exports(new_module, *headers):
        if (
            function.module.export_directory_rva
            <= function.rva
            <= function.module.export_directory_rva
            + function.module.export_directory_size
        ):
            forwarded_functions.append(function)
            continue

        Hooks.name_hooks[
            function.module_name.upper() + "|" + function.name
        ] = function
        functions[str(base_address) + "|" + function.name] = function
        # if function.rva != cast(function.export_address, POINTER(c_uint32)).contents.value:
        #     print(function)
        hook_function(function)

    return forwarded_functions


def resolve_ordinal(module: MODULEENTRY32, ordinal: int) -> int:
    """
    This function resolves the address for an ordinal.
    """

    return cast(
        addressof(module.modBaseAddr.contents)
        + module.export_directory.AddressOfFunctions,
        POINTER(c_uint32 * module.export_directory.NumberOfFunctions),
    ).contents[ordinal - 1]


def resolve_module_by_address(
    base_address: int,
    hooks: Dict[str, Function],
    imports: List[ImportFunction],
) -> MODULEENTRY32:
    """
    This function returns the module for the base address sent as argument.
    """

    if module := modules.get(base_address):
        return module

    for module in list_modules():
        if base_address == addressof(module.modBaseAddr.contents):
            hooks_forwarded(hooks_DLL(module, hooks, imports), hooks, imports)
            return modules[base_address]


def hooks_forwarded(
    functions: List[Function],
    hooks: Dict[str, Function],
    imports: List[ImportFunction],
    count: int = 0,
) -> None:
    """
    This function hooks forwarded functions.
    """

    functions_copy = functions.copy()

    for function in functions:
        module_name, function_name = (
            c_char_p(function.address).value.decode().split(".")
        )
        module = None

        base_address = LoadLibraryW(module_name)
        if base_address is not None:
            module = resolve_module_by_address(base_address, hooks, imports)
        if function_name[0] == "#":
            function.address = resolve_ordinal(module, int(function_name[1:]))
        else:
            target_function = hooks.get(
                str(base_address) + "|" + function_name
            )
            if target_function is None:
                address = GetProcAddress(
                    GetModuleHandleW(function.module_name),
                    function.name.encode(),
                )
                if not address:
                    continue
                function.address = address
            else:
                function.address = target_function.address

        Hooks.name_hooks[
            function.module_name.upper() + "|" + function.name
        ] = function
        hooks[
            str(addressof(function.module.modBaseAddr.contents))
            + "|"
            + function.name
        ] = function

        # function.module = target_function.module

        hook_function(function)
        functions_copy.remove(function)

    if functions_copy and count != len(functions_copy):
        hooks_forwarded(functions_copy, hooks, imports, len(functions_copy))


def hooks_DLLs() -> Dict[str, Function]:
    """
    This function hooks all loaded modules (imported DLLs):
        - EAT (Export Address Table) functions addresses,
        - Configured IAT (Import Address Table) functions addresses.
    """

    functions = {}
    imports = []
    forwarded = []

    for module in list_modules():
        forwarded.extend(hooks_DLL(module, functions, imports))

    hooks_forwarded(forwarded, functions, imports)
    hooks_IAT(imports, False)
    return functions


def hooks_IAT(
    imports: List[ImportFunction], is_target: bool = True
) -> Dict[str, ImportFunction]:
    """
    This function hooks the IAT (Import Address Table) functions.
    """

    for i, function in enumerate(imports):
        if not is_target:
            if (
                function.module_container.lower()
                == basename(executable).lower()
                or function.module_container.lower().endswith(".pyd")
                or fullmatch(
                    r"python\d+\.dll", function.module_container.lower()
                )
            ):
                continue
            if (
                function.name
                not in CallbackManager.config["import_loaded_module_hooks"]
            ):
                continue

        build_generic_callback("IAT", function)
        Hooks.import_hooks[
            f"{function.module}|{function.name}|{function.module_container}"
        ] = function

        hook_pointer = cast(function.hook, c_void_p).value
        write_in_memory(
            function.import_address,
            hook_pointer.to_bytes(sizeof(c_void_p), byteorder="little"),
        )

    return Hooks.import_hooks


def load(file: _BufferedIOBase) -> None:
    """
    This function is based on: https://github.com/mauricelambert/PyPeLoader/blob/af116589d379220b7c886fffc146cc7dd7b91732/PyPeLoader.py#L628

    This function does all steps to load, hooks functions (EAT and IAT) and
    execute the PE program in memory.
    """

    pe_headers = load_headers(file)
    image_base = load_in_memory(file, pe_headers)
    file.close()

    imports = get_imports(pe_headers, image_base, "target")
    Hooks.import_hooks = hooks_IAT(imports)
    Hooks.export_hooks = hooks_DLLs()
    load_relocations(pe_headers, image_base)

    function_type = CFUNCTYPE(c_int)
    function = function_type(
        image_base + pe_headers.optional.AddressOfEntryPoint
    )
    CallbackManager.run = get_native_id()
    function()


def config():
    """
    This function loads configurations in CallbackManager.
    """

    with open("config.json") as file:
        config = json_load(file)

    CallbackManager.config = config
    return config


def main() -> int:
    """
    This function is based on: https://github.com/mauricelambert/PyPeLoader/blob/af116589d379220b7c886fffc146cc7dd7b91732/PyPeLoader.py#L647

    This function is the main function to start the script
    from the command line.
    """

    if len(argv) <= 1:
        print(
            'USAGES: "',
            executable,
            '" "',
            argv[0],
            '" executable_path',
            sep="",
            file=stderr,
        )
        return 1

    config()
    load(open(argv[1], "rb"))
    return 0


if __name__ == "__main__":
    exit(main())

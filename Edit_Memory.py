from ctypes import *
from ctypes import wintypes as w
import struct


def read_address(pid, address):
    k32 = windll.kernel32

    open_process = k32.OpenProcess
    open_process.arg_types = [w.DWORD, w.BOOL, w.DWORD]
    open_process.restype = w.HANDLE

    read_process_memory = k32.ReadProcessMemory
    read_process_memory.arg_types = [w.HANDLE, w.LPCVOID, w.LPVOID, c_size_t, POINTER(c_size_t)]
    read_process_memory.restype = w.BOOL

    GetLastError = k32.GetLastError
    GetLastError.arg_types = None
    GetLastError.restype = w.DWORD

    close_handle = k32.CloseHandle
    close_handle.arg_types = [w.HANDLE]
    close_handle.restype = w.BOOL

    process_handle = open_process(0x10, False, pid)

    if address[1] == 1:
        data = c_ubyte()
    elif address[1] == 2:
        data = c_ushort()
    elif address[1] == 4:
        data = c_ulong()
    else:
        data = c_ulonglong

    bytes_read = c_ulonglong()
    read_process_memory(process_handle, address[0], byref(data), sizeof(data), byref(bytes_read))
    close_handle(process_handle)
    return data.value


def write_address(pid, address, value):
    open_process = windll.kernel32.OpenProcess
    write_process_memory = windll.kernel32.WriteProcessMemory
    close_handle = windll.kernel32.CloseHandle

    process_all_access = 0x1F0FFF

    size_lib = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    data_dummy = struct.pack(size_lib[address[1]], value)
    buffer = c_char_p(data_dummy)
    buffer_size = address[1]
    bytes_read = c_ulong(0)

    process_handle = open_process(process_all_access, False, int(pid))

    write_process_memory(process_handle, address[0], buffer, buffer_size, byref(bytes_read))

    close_handle(process_handle)



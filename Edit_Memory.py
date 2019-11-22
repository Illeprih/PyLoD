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

    CloseHandle = k32.CloseHandle
    CloseHandle.arg_types = [w.HANDLE]
    CloseHandle.restype = w.BOOL

    processHandle = open_process(0x10, False, pid)

    if address[1] == 1:
        data = c_ubyte()
    elif address[1] == 2:
        data = c_ushort()
    elif address[1] == 4:
        data = c_ulong()
    else:
        data = c_ulonglong

    bytes_read = c_ulonglong()
    read_process_memory(processHandle, address[0], byref(data), sizeof(data), byref(bytes_read))
    CloseHandle(processHandle)
    return data.value


def write_address(pid, address, value):
    OpenProcess = windll.kernel32.OpenProcess
    WriteProcessMemory = windll.kernel32.WriteProcessMemory
    CloseHandle = windll.kernel32.CloseHandle

    PROCESS_ALL_ACCESS = 0x1F0FFF

    size_lib = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    datadummy = struct.pack(size_lib[address[1]], value)
    buffer = c_char_p(datadummy)
    bufferSize = address[1]
    bytesRead = c_ulong(0)

    processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

    WriteProcessMemory(processHandle, address[0], buffer, bufferSize, byref(bytesRead))

    CloseHandle(processHandle)



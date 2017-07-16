"""
Memory read/write module for Python 3x
Abstracts the use of win32 api in order to
read and write memory of processes
Does not need to be run with Administrator privileges,
unless you want to access memory of privileged programs

using a process handle of -1 will read/write python's own memory

WARNING: You can damage your system and lose data
when messing with memory. Be careful.

Also note that generally read and write have a some small overhead.
"""

import struct
# Using explicit imports
from ctypes import c_char_p, c_size_t, c_char,\
    windll, WinDLL, POINTER, \
    get_last_error, set_last_error,\
    create_string_buffer, byref,\
    cast

from ctypes.wintypes import HANDLE, LPVOID, LPCVOID, BOOL

import psutil

__author__ = "SamsonPianoFingers"
__credits__ = ["SamsonPianoFingers"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "SamsonPianoFingers"
__email__ = "itsthatguyagain3@gmail.com"
__status__ = "Prototype"

#  constants
PROCESS_ALL_ACCESS = 0x1F0FFF
SIZE_DOUBLE = 8
SIZE_LONGLONG = 8
SIZE_FLOAT = 4
SIZE_LONG = 4
SIZE_INT = 4
SIZE_SHORT = 2
SIZE_CHAR = 1

# windows error code list - >
# msdn.microsoft.com/en-us/library/windows/desktop/ms681382(v=vs.85).aspx
ERR_CODE = {
    5: "ERROR_ACCESS_DENIED",
    6: "ERROR_INVALID_HANDLE",
    87: "ERROR_INVALID_PARAMETER",
    299: "ERROR_PARTIAL_COPY",
    487: "ERROR_INVALID_ADDRESS",
    998: "ERROR_NOACCESS"
}

# ACCESS_DENIED is a priveledge issue
# INVALID_HANDLE means process handle is not valid
# PARTIAL_COPY means that either some or none of the memory was copied
# this may be because memory is not committed at that address


# Create w32api references
__rPM__ = WinDLL('kernel32', use_last_error=True).ReadProcessMemory
__rPM__.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
__rPM__.restype = BOOL

__wPM__ = WinDLL('kernel32', use_last_error=True).WriteProcessMemory
__wPM__.argtypes = [HANDLE, LPVOID, LPCVOID, c_size_t, POINTER(c_size_t)]
__wPM__.restype = BOOL

__OpenProcess__ = windll.kernel32.OpenProcess
__CloseHandle__ = windll.kernel32.CloseHandle


def open_process(pid):
    """Gets a handle to the process id (pid) of the target process
    Returns the handle (int), on failure returns None

    Keyword arguments:
    pid -- process id of process to open (int)
    """
    process_handle = __OpenProcess__(PROCESS_ALL_ACCESS, 0, pid)
    if process_handle != 0:
        return process_handle
    return None


def open_process_name(name):
    """Gets a handle to the first process found with specified name
    Process names are case sensitive
    Returns the handle (int), on failure returns None

    Keyword arguments:
    pid -- process id of process to open (int)
    """
    for i in psutil.process_iter():
        if i.name() == name:
            return open_process(i.pid)
    return None


def close_process(process_handle):
    """Closes the handle to a process

    Keyword arguments:
    process_handle -- handle to process
    """
    __CloseHandle__(process_handle)


def read_integer(process_handle, address):
    """Reads an int at a specified address from a process
    Returns an int which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_INT)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, SIZE_INT, byref(bytes_read))
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return struct.unpack("I", buffer[0:SIZE_INT])[0]


def read_short(process_handle, address):
    """Reads an short at a specified address from a process
    Returns an short which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_SHORT)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, SIZE_SHORT, byref(bytes_read))
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return struct.unpack("H", buffer[0:SIZE_SHORT])[0]


def read_byte(process_handle, address):
    """Reads a single byte at a specified address from a process
    Returns an byte which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_CHAR)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, SIZE_CHAR, byref(bytes_read))
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return struct.unpack("B", buffer[0:SIZE_CHAR])[0]


def read_bytes(process_handle, address, length):
    """Reads an array of bytes at a specified address from a process
    Returns a list which is values at [address], with a length of [length]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    length -- number of bytes to read
    """
    buffer = create_string_buffer(length)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, length, byref(bytes_read))
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return bytearray(buffer[0:length])


def read_float(process_handle, address):
    """Reads a single float at a specified address from a process
    Returns an float which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_FLOAT)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, SIZE_FLOAT, byref(bytes_read))
    err = get_last_error()
    set_last_error(0)
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return struct.unpack("f", buffer[0:SIZE_FLOAT])[0]


def read_double(process_handle, address):
    """Reads a single double at a specified address from a process
    Returns an double which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_DOUBLE)
    bytes_read = c_size_t()
    __rPM__(process_handle, address, buffer, SIZE_DOUBLE, byref(bytes_read))
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))
    return struct.unpack("d", buffer[0:SIZE_DOUBLE])[0]


def write_integer(process_handle, address, value):
    """Writes a single int at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("I", value))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, SIZE_INT, None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def write_short(process_handle, address, value):
    """Writes a single short at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("H", value))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, SIZE_SHORT, None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def write_float(process_handle, address, value):
    """Writes a single float at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("f", value))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, SIZE_FLOAT, None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def write_double(process_handle, address, value):
    """Writes a single double at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("d", value))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, SIZE_DOUBLE, None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def write_byte(process_handle, address, value):
    """Writes a single byte at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("B", value))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, SIZE_CHAR, None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def write_bytes(process_handle, address, buffer):
    """Writes a buffer (number of bytes) to a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    buffer -- a bytearray or bytes object to write at [address]
    """
    c_data = c_char_p(bytes(buffer))
    c_data_ = cast(c_data, POINTER(c_char))
    __wPM__(process_handle, address, c_data_, len(buffer), None)
    err = get_last_error()
    if err:
        set_last_error(0)
        #print(ERR_CODE.get(err, err))


def resolve_multi_pointer(process_handle, base_address, offset_list):
    """Resolves a multi-level pointer to an address.
    Returns an address as (int)

    Keyword arguments:
    process_handle -- handle to process
    base_address -- base address of pointer
    offset_list -- a list of offsets (ints)
    """
    resolved_ptr = base_address
    for i in offset_list:
        resolved_ptr = read_integer(process_handle, resolved_ptr) + i
    return resolved_ptr


def resolve_pointer(process_handle, base_address, offset):
    """Resolves a single level pointer to an address.
    Returns an address as (int)

    Keyword arguments:
    process_handle -- handle to process
    base_address -- base address of pointer
    offset -- pointer offset
    """
    return read_integer(process_handle, base_address) + offset

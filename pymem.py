# !/usr/bin/env python
"""
Abstracts the use of win32 api in order to
read and write memory of processes
Does not need to be run with Administrator privileges,
unless you want to access memory of privileged programs

WARNING: You can damage your system and lose data
when messing with memory. Be careful.

Also note that generally read and write have a some small overhead.
Module Functions:
openProc(pid)
openProcName(name)
closeProc(process_handle)

readInt(process_handle, address)
readShort(process_handle, address)
readByte(process_handle, address)
readBytes(process_handle, address, length)
readFloat(process_handle, address)
readDouble(process_handle, address)

writeInt(process_handle, address, value)
writeShort(process_handle, address, value)
writeFloat(process_handle, address, value)
writeDouble(process_handle, address, value)
writeByte(process_handle, address, value)
writeBytes(process_handle, address, buffer)
resolveMultiPointer(process_handle, base_address, offset_list):
resolvePointer(process_handle, base_address, offset):
"""

import struct

import psutil

__author__ = "SamsonPianoFingers"
__credits__ = ["SamsonPianoFingers"]
__license__ = "GPL"
__version__ = "0.1"
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

# msdn.microsoft.com/en-us/library/windows/desktop/ms681382(v=vs.85).aspx
ERR_CODE = {
    5: "ERROR_ACCESS_DENIED",
    6: "ERROR_INVALID_HANDLE",
    87: "ERROR_INVALID_PARAMETER",
    299: "ERROR_PARTIAL_COPY",
    487: "ERROR_INVALID_ADDRESS",
    998: "ERROR_NOACCESS"
}


# Create w32api references
rPM = WinDLL('kernel32', use_last_error=True).ReadProcessMemory
rPM.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
rPM.restype = BOOL

wPM = WinDLL('kernel32', use_last_error=True).WriteProcessMemory
wPM.argtypes = [HANDLE, LPVOID, LPCVOID, c_size_t, POINTER(c_size_t)]
wPM.restype = BOOL

OpenProcess = windll.kernel32.OpenProcess
CloseHandle = windll.kernel32.CloseHandle


def openProc(pid):
    Returns the handle (int), on failure returns -1

    Keyword arguments:
    pid -- process id of process to open (int)
    """
    process_handle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
    if(process_handle != 0):
        return process_handle
    else:
        return -1


def openProcName(name):
    for i in psutil.process_iter():
        if(i.name() == name):
            return openProc(i.pid)
    return -1


def closeProc(process_handle):
    """Closes the handle to a process

    Keyword arguments:
    process_handle -- handle to process
    """
    CloseHandle(process_handle)


def readInt(process_handle, address):
    """Reads an int at a specified address from a process
    Returns an int which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_INT)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, SIZE_INT, byref(bytes_read))
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))
    return struct.unpack("I", buffer[0:SIZE_INT])[0]


def readShort(process_handle, address):
    """Reads an short at a specified address from a process
    Returns an short which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_SHORT)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, SIZE_SHORT, byref(bytes_read))
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))
    return struct.unpack("H", buffer[0:SIZE_SHORT])[0]


def readByte(process_handle, address):
    """Reads a single byte at a specified address from a process
    Returns an byte which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_CHAR)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, SIZE_CHAR, byref(bytes_read))
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))
    return struct.unpack("B", buffer[0:SIZE_CHAR])[0]


def readBytes(process_handle, address, length):
    """Reads an array of bytes at a specified address from a process
    Returns a list which is values at [address], with a length of [length]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    length -- number of bytes to read
    """
    buffer = create_string_buffer(length)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, length, byref(bytes_read))
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))
    return bytearray(buffer[0:length])


def readFloat(process_handle, address):
    """Reads a single float at a specified address from a process
    Returns an float which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_FLOAT)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, SIZE_FLOAT, byref(bytes_read))
    err = get_last_error()
    set_last_error(0)
    if(err):
        print(ERR_CODE.get(err, err))
    return struct.unpack("f", buffer[0:SIZE_FLOAT])[0]


def readDouble(process_handle, address):
    """Reads a single double at a specified address from a process
    Returns an double which is the value at [address]

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to read from
    """
    buffer = create_string_buffer(SIZE_DOUBLE)
    bytes_read = c_size_t()
    rPM(process_handle, address, buffer, SIZE_DOUBLE, byref(bytes_read))
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))
    return struct.unpack("d", buffer[0:SIZE_DOUBLE])[0]


def writeInt(process_handle, address, value):
    """Writes a single int at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("I", value))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, SIZE_INT, None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def writeShort(process_handle, address, value):
    """Writes a single short at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("H", value))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, SIZE_SHORT, None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def writeFloat(process_handle, address, value):
    """Writes a single float at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("f", value))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, SIZE_FLOAT, None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def writeDouble(process_handle, address, value):
    """Writes a single double at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("d", value))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, SIZE_DOUBLE, None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def writeByte(process_handle, address, value):
    """Writes a single byte at a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    value -- value to write at [address]
    """
    c_data = c_char_p(struct.pack("B", value))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, SIZE_CHAR, None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def writeBytes(process_handle, address, buffer):
    """Writes a buffer (number of bytes) to a specified address in a process

    Keyword arguments:
    process_handle -- handle to process
    address -- address in process to write to
    buffer -- a bytearray or bytes object to write at [address]
    """
    c_data = c_char_p(bytes(buffer))
    c_data_ = cast(c_data, POINTER(c_char))
    wPM(process_handle, address, c_data_, len(buffer), None)
    err = get_last_error()
    if(err):
        set_last_error(0)
        print(ERR_CODE.get(err, err))


def resolveMultiPointer(process_handle, base_address, offset_list):
    """Resolves a multi-level pointer to an address.
    Returns an address as (int)

    Keyword arguments:
    process_handle -- handle to process
    base_address -- base address of pointer
    offset_list -- a list of offsets (ints)
    """
    resolved_ptr = base_address
    for i in offset_list:
        resolved_ptr = readInt(process_handle, resolved_ptr) + i
    return resolved_ptr


def resolvePointer(process_handle, base_address, offset):
    """Resolves a single level pointer to an address.
    Returns an address as (int)

    Keyword arguments:
    process_handle -- handle to process
    base_address -- base address of pointer
    offset -- pointer offset
    """
    return readInt(process_handle, base_address) + i

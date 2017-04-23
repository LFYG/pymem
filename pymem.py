#external dependencies include psutil (install with pip/pip3)
#or disable openProcName and remove psutil import

import sys, ctypes, struct, psutil
import ctypes.wintypes as wintypes
"""
Memory read/write module for Python 3x (untested with 2x)
Abstracts and simplifies the use of win32 api
in order to read and write memory of processes
Needs to be run with Administrator privileges.

WARNING: You can damage your system and lose data
when messing with memory. Be careful.

Also note that read and write have a some overhead (slow functions).
Module Functions:
openProc(pid)
openProcName(name)
closeProc(procHandle)

readInt(procHandle, address)
readShort(procHandle, address)
readByte(procHandle, address)
readBytes(procHandle, address, length)
readFloat(procHandle, address)
readDouble(procHandle, address)

writeInt(procHandle, address, value)
writeShort(procHandle, address, value)
writeFloat(procHandle, address, value)
writeDouble(procHandle, address, value)
writeByte(procHandle, address, value)
writeBytes(procHandle, address, buffer)

resolvePointer(procHandle, base_address, offset_list)
"""

#Define constants
SIZE_DOUBLE = 8
SIZE_LONGLONG = 8
SIZE_FLOAT = 4;
SIZE_LONG = 4;
SIZE_INT = 4;
SIZE_SHORT = 2;
SIZE_CHAR = 1
PROCESS_ALL_ACCESS = 0x1F0FFF

#Create function references for simple use
rPM = ctypes.WinDLL('kernel32',use_last_error=True).ReadProcessMemory
rPM.argtypes = [wintypes.HANDLE,wintypes.LPCVOID,wintypes.LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
rPM.restype = wintypes.BOOL

wPM = ctypes.WinDLL('kernel32',use_last_error=True).WriteProcessMemory
wPM.argtypes = [wintypes.HANDLE,wintypes.LPVOID,wintypes.LPCVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
wPM.restype = wintypes.BOOL

OpenProcess = ctypes.windll.kernel32.OpenProcess

CloseHandle = ctypes.windll.kernel32.CloseHandle

def openProc(pid):
	"""Creates a handle to the process id (pid) of the target process
	Returns the handle (int), on failure returns -1
	
	Keyword arguments:
	pid -- process id of process to open (int)
	"""
	procHandle = OpenProcess(PROCESS_ALL_ACCESS,0,pid)
	if(procHandle!=0):
		return procHandle
	return -1

def openProcName(name):
	for i in psutil.process_iter():
		if(i.name() == name):
			return openProc(i.pid)
	return -1

def closeProc(procHandle):
	"""Closes the handle to a process
	
	Keyword arguments:
	procHandle -- handle to process
	"""
	CloseHandle(procHandle)
	
def readInt(procHandle, address):
	"""Reads an int at a specified address from a process
	Returns an int which is the value at [address]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	"""
	buffer = ctypes.create_string_buffer(SIZE_INT)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,SIZE_INT,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return struct.unpack("i",buffer[0:SIZE_INT])[0]
	
def readShort(procHandle, address):
	"""Reads an short at a specified address from a process
	Returns an short which is the value at [address]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	"""
	buffer = ctypes.create_string_buffer(SIZE_SHORT)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,SIZE_SHORT,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return struct.unpack("h",buffer[0:SIZE_SHORT])[0]
	
def readByte(procHandle, address):
	"""Reads a single byte at a specified address from a process
	Returns an byte which is the value at [address]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	"""
	buffer = ctypes.create_string_buffer(SIZE_CHAR)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,SIZE_CHAR,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return struct.unpack("b",buffer[0:SIZE_CHAR])[0]
	
def readBytes(procHandle, address, length):
	"""Reads an array of bytes at a specified address from a process
	Returns an an array which is values at [address], with a length of [length]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	length -- number of bytes to read
	"""
	buffer = ctypes.create_string_buffer(length)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,length,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return bytearray(buffer[0:length])
	
def readFloat(procHandle, address):
	"""Reads a single float at a specified address from a process
	Returns an float which is the value at [address]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	"""
	buffer = ctypes.create_string_buffer(SIZE_FLOAT)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,SIZE_FLOAT,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return struct.unpack("f",buffer[0:SIZE_FLOAT])[0]

def readDouble(procHandle, address):
	"""Reads a single double at a specified address from a process
	Returns an double which is the value at [address]
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to read from
	"""
	buffer = ctypes.create_string_buffer(SIZE_DOUBLE)
	bytes_read = ctypes.c_size_t()
	rPM(procHandle,address,buffer,SIZE_DOUBLE,ctypes.byref(bytes_read))
	err = ctypes.get_last_error()
	return struct.unpack("d",buffer[0:SIZE_DOUBLE])[0]

def writeInt(procHandle, address, value):
	"""Writes a single int at a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	value -- value to write at [address]
	"""
	c_data = ctypes.c_char_p(struct.pack("i",value))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, SIZE_INT, None)

def writeShort(procHandle, address, value):
	"""Writes a single short at a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	value -- value to write at [address]
	"""
	c_data = ctypes.c_char_p(struct.pack("h",value))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, SIZE_SHORT, None)

def writeFloat(procHandle, address, value):
	"""Writes a single float at a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	value -- value to write at [address]
	"""
	c_data = ctypes.c_char_p(struct.pack("f",value))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, SIZE_FLOAT, None)

def writeDouble(procHandle, address, value):
	"""Writes a single double at a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	value -- value to write at [address]
	"""
	c_data = ctypes.c_char_p(struct.pack("d",value))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, SIZE_DOUBLE, None)
	
def writeByte(procHandle, address, value):
	"""Writes a single byte at a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	value -- value to write at [address]
	"""
	c_data = ctypes.c_char_p(struct.pack("b",value))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, SIZE_CHAR, None)
	
def writeBytes(procHandle, address, buffer):
	"""Writes a buffer (number of bytes) to a specified address in a process
	
	Keyword arguments:
	procHandle -- handle to process
	address -- address in process to write to
	buffer -- a bytearray or bytes object to write at [address]
	"""
	c_data = ctypes.c_char_p(bytes(buffer))
	c_data_ = ctypes.cast(c_data,ctypes.POINTER(ctypes.c_char))
	wPM(procHandle, address, c_data_, len(buffer), None)

def resolvePointer(procHandle, base_address, offset_list):
	"""Resolves a pointer or multi-level pointer to an address.
	Returns an address as (int)
	
	Keyword arguments:
	procHandle -- handle to process
	base_address -- base address of pointer
	offset_list -- a list of offsets (ints) for multi-level pointers
	or single level pointers (one item in list)
	"""
	resolved_ptr = base_address
	for i in offset_list:
		resolved_ptr = readInt(procHandle,resolved_ptr)+i
	return resolved_ptr
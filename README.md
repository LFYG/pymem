# pymem
Proof of concept python module for read/write to process memory<br>
Abstracts and simplifies the use of win32 api in order to read and write memory of processes<br>
Python programs that import pymem need to be run with Administrator privileges<br>
This limitation does not have a workaround currently<br>
<br>

# pymem User Functions
```python

def openProc(pid)
def openProcName(name)
def closeProc(process_handle)
def readInt(process_handle, address)
def readShort(process_handle, address)
def readByte(process_handle, address)
def readBytes(process_handle, address, length)
def readFloat(process_handle, address)
def readDouble(process_handle, address)
def writeInt(process_handle, address, value)
def writeShort(process_handle, address, value)
def writeFloat(process_handle, address, value)
def writeDouble(process_handle, address, value)
def writeByte(process_handle, address, value)
def writeBytes(process_handle, address, buffer)
def resolvePointer(process_handle, base_address, offset)
def resolveMultiPointer(process_handle, base_address, offset_list)
```
# pymem Internal Functions
```python

OpenProcess(pid)
CloseHandle(handle)
rPM(procHandle,address,buffer,length,bytes_read)
wPM(procHandle,address,c_data, length,bytes_written)
```
and a sister project...<br>
# pyscan
Proof of concept memory scanner module for python (like cheat engine). Relies on mempy<br>
Currently very slow and poorly written<br>

# pyscan User Functions
```python
def init_scan(process_handle, value, scan_type, memory_protection)
def scan_page_int(process_handle, region, value)
def scan_page_short(process_handle, region, value)
def scan_page_byte(process_handle, region, value)
def scan_page_float(process_handle, region, value)
def scan_page_double(process_handle, region, value)
def rescan_equal(process_handle, addresses, value, scan_type)
def rescan_not(process_handle, addresses, value, scan_type)
def rescan_bigger_than(process_handle, addresses, value, scan_type)
def rescan_less_than(process_handle, addresses, value, scan_type)
```
# pyscan Internal functions
```python
def VirtualQueryEx(process_handle, address)
def GetMemoryRegions(process_handle)
```
along with a new module...<br>

# pytrainer
A module that contains classes and functions useful for creating trainers in python<br>
Uses pymem<br>
# pytrainer Functions and Classes
```python
def set_process(process)
def release_process()
class Address()
	__init__(self, address, type)
	read(self)
	write(self, value)
	lock(self, value, interval = 0.25)
	unlock(self)
	
class Pointer()
	__init__(self, base_address, offset_list, type)
	resolve(self)
	read(self)
	write(self, value)
	resolve_and_read(self)
	resolve_and_write(self, value)
	lock(self, value, interval = 0.25)
	unlock(self)
	
class Patch()
	__init__(self, address, patch_bytes)
	patch_bytes()
	restore_bytes()
```

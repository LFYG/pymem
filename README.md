# pymem
Proof of concept python module for read/write to process memory<br>

Abstracts and simplifies the use of win32 api<br><br>
In order to read and write memory of processes<br>
Python programs that import pymem need to be run with Administrator privileges<br>
This limitation does not have a workaround currently<br>

# Functions
openProc(pid)<br>
openProcName(name)<br>
closeProc(process_handle)<br>
readInt(process_handle, address)<br>
readShort(process_handle, address)<br>
readByte(process_handle, address)<br>
readBytes(process_handle, address, length)<br>
readFloat(process_handle, address)<br>
readDouble(process_handle, address)<br>
writeInt(process_handle, address, value)<br>
writeShort(process_handle, address, value)<br>
writeFloat(process_handle, address, value)<br>
writeDouble(process_handle, address, value)<br>
writeByte(process_handle, address, value)<br>
writeBytes(process_handle, address, buffer)<br>
resolvePointer(process_handle, base_address, offset)<br>
resolveMultiPointer(process_handle, base_address, offset_list):<br>
<br>
and a sister project...<br>
# pyscan
Proof of concept memory scanner module for python (like cheat engine). Relies on mempy<br>
Currently very slow and poorly written<br>
# pyscan Functions
scan_page_int(process_handle, region, value)<br>
scan_page_short(process_handle, region, value)<br>
scan_page_byte(process_handle, region, value)<br>
scan_page_float(process_handle, region, value)<br>
scan_page_double(process_handle, region, value)<br>
rescan_equal(process_handle, addresses, value, scan_type)<br>
rescan_not(process_handle, addresses, value, scan_type)<br>
rescan_bigger_than(process_handle, addresses, value, scan_type)<br>
rescan_less_than(process_handle, addresses, value, scan_type)<br><br>

along with a new module...<br>
# pytrainer
A module that contains classes and functions useful for creating trainers in python<br>
Uses pymem<br>
# ptrainer Functions and Classes
set_process(process)<br>
release_process()<br>
class Address()<br>
	__init__(self, address, type)<br>
	read(self)<br>
	write(self, value)<br>
	lock(self, value, interval = 0.25)<br>
	unlock(self)<br>
	<br>
class Pointer()<br>
	__init__(self, base_address, offset_list, type)<br>
	resolve(self)<br>
	read(self)<br>
	write(self, value)<br>
	resolve_and_read(self)<br>
	resolve_and_write(self, value)<br>
	lock(self, value, interval = 0.25)<br>
	unlock(self)<br>
	<br>
class Patch()<br>
	__init__(self, address, patch_bytes)<br>
	patch_bytes()<br>
	restore_bytes()<br>
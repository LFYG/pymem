# pymem
Proof of concept python module for read/write to process memory<br>

Abstracts and simplifies the use of win32 api<br><br>
In order to read and write memory of processes<br>
Python programs that import pymem need to be run with Administrator privileges<br>
This limitation does not have a workaround currently<br>
<br>
Full Docstring documentation coming soon™....

# pymem User Functions
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

# pymem Internal Functions
OpenProcess(pid)<br>
CloseHandle(handle)<br>
rPM(procHandle,address,buffer,length,bytes_read)<br>
wPM(procHandle,address,c_data, length,bytes_written)<br><br>

and a sister project...<br>
# pyscan
Proof of concept memory scanner module for python (like cheat engine). Relies on mempy<br>

# pyscan User Functions
init_scan(process_handle, value, scan_type, memory_protection)<br>
scan_page_int(process_handle, region, value)<br>
scan_page_short(process_handle, region, value)<br>
scan_page_byte(process_handle, region, value)<br>
scan_page_float(process_handle, region, value)<br>
scan_page_double(process_handle, region, value)<br>
rescan_equal(process_handle, addresses, value, scan_type)<br>
rescan_not(process_handle, addresses, value, scan_type)<br>
rescan_bigger_than(process_handle, addresses, value, scan_type)<br>
rescan_less_than(process_handle, addresses, value, scan_type)<br>

# pyscan Internal functions
VirtualQueryEx(process_handle, address)<br>
GetMemoryRegions(process_handle)<br>

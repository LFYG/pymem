# pymem
Tiny python module for read/write to process memory<br>

Abstracts and simplifies the use of win32 api<br><br>
In order to read and write memory of processes<br>
Python programs that import pymem need to be run with Administrator privileges<br>
This limitation does not have a workaround currently<br>

# Functions
openProc(pid)<br>
openProcName(name)<br>
closeProc(procHandle)<br>
readInt(procHandle, address)<br>
readShort(procHandle, address)<br>
readByte(procHandle, address)<br>
readBytes(procHandle, address, length)<br>
readFloat(procHandle, address)<br>
readDouble(procHandle, address)<br>
writeInt(procHandle, address, value)<br>
writeShort(procHandle, address, value)<br>
writeFloat(procHandle, address, value)<br>
writeDouble(procHandle, address, value)<br>
writeByte(procHandle, address, value)<br>
writeBytes(procHandle, address, buffer)<br>
resolvePointer(procHandle, base_address, offset_list)<br>

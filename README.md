# Closure of this project - to the few that knew about it
 I'm sorry to say that this project has now been closed but will stay available for reference.
 
 It was fun to make and exciting to explore this field of programming
 
 The closure is due to the realisation that this far better project exists: https://github.com/srounet/Pymem

# pymem
Proof of concept python module for read/write to process memory<br>
Abstracts and simplifies the use of win32 api in order to read and write memory of processes<br>
Only supports windows currently - working on linux version.
Support for other OS's will have to wait for a while.
<br>

# pymem module API
```python

open_process(pid)
open_process_name(name)
close_process(process_handle)
read_integer(process_handle, address)
read_short(process_handle, address)
read_byte(process_handle, address)
read_bytes(process_handle, address, length)
read_float(process_handle, address)
read_double(process_handle, address)
write_integer(process_handle, address, value)
write_short(process_handle, address, value)
write_float(process_handle, address, value)
write_double(process_handle, address, value)
write_byte(process_handle, address, value)
write_bytes(process_handle, address, buffer)
resolve_multi_pointer(process_handle, base_address, offset)
resolve_pointer(process_handle, base_address, offset_list)
```
# pymem Internal Functions
```python

OpenProcess(pid)
__CloseHandle__(handle)
__rPM__(process_handle ,address, buffer, length, bytes_read)
__wPM__(process_handle ,address, c_data, length, bytes_written)
```
and sister projects...<br>

# pytrainer
A module for creating trainers in python<br>
Uses pymem<br>

# pyregion
A module for getting information on memory regions in processes

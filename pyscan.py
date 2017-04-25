#Proof of concept (not very good) memory scanner for python 3
#reference code by Cadaver (for python 2.7), (WHICH IS HUGELY BETTER THAN MY CODE)
#http://www.rohitab.com/discuss/topic/39525-process-memory-scannerpy/
#credit for portions of this code go to Cadaver at
#http://www.rohitab.com/discuss/user/14859-cadaver/
#I want to write my version differently to cadaver
#I also want to rewrite it so that it uses ctypes for the scanning values as well.
#this example is quite messy, and I am going to do a lot of
#planning and rewrite this monsta. Its not even object oriented, just a list of functions
#pymem module was written by myself.
#This POC was mainly me just exploring if what i wanted to do was possible in python 3.
#also it has no proper error checking :( and niether does pymem

import pymem
import struct
from ctypes import *
from ctypes.wintypes import *

#memory_information_types
MEM_STATES = {
0x1000 : "MEM_COMMIT",
0x10000: "MEM_FREE",
0x2000:"MEM_RESERVE"
}
MEM_PROTECTIONS = {
0x10: "PAGE_EXECUTE",
0x20: "PAGE_EXECUTE_READ",
0x40: "PAGE_EXECUTE_READWRITE",
0x80: "PAGE_EXECUTE_WRITECOPY",
0x01: "PAGE_NOACCESS",
0x04: "PAGE_READWRITE",
0x08: "PAGE_WRITECOPY"
}
MEM_TYPES = {
0x1000000: "MEM_IMAGE",
0x40000: "MEM_MAPPED",
0x20000: "MEM_PRIVATE"
}

#scan_types
type_int = 0
type_short = 1
type_byte = 2
type_float = 3
type_double = 4

#structs
class MEMORY_BASIC_INFORMATION(Structure):
	_fields_ = [
	("BaseAddress", c_void_p),
	("AllocationBase", c_void_p),
	("AllocationProtect", DWORD),
	("RegionSize", c_size_t),
	("State", DWORD),
	("Protect", DWORD),
	("Type", DWORD)]
	
class PyMEMORY_BASIC_INFORMATION:

	def __init__ (self, MBI):
		self.MBI = MBI
		self.BaseAddress = self.MBI.BaseAddress
		self.AllocationBase = self.MBI.AllocationBase
		self.AllocationProtect = MEM_PROTECTIONS.get (self.MBI.AllocationProtect, self.MBI.AllocationProtect)
		self.RegionSize = self.MBI.RegionSize
		self.State = MEM_STATES.get (self.MBI.State, self.MBI.State)
		self.Protect = MEM_PROTECTIONS.get (self.MBI.Protect, self.MBI.Protect)
		self.Type = MEM_TYPES.get (self.MBI.Type, self.MBI.Type)
	
class SYSTEM_INFO(Structure):
    _fields_ = [
	("ProcessorArchitecture", WORD),
	("Reserved", WORD),
	("PageSize", DWORD),
	("MinimumApplicationAddress", DWORD),
	("MaximumApplicationAddress", DWORD),
	("ActiveProcessorMask", DWORD),
	("NumberOfProcessors", DWORD),
	("ProcessorType", DWORD),
	("AllocationGranularity", DWORD),
	("ProcessorLevel", WORD),
	("ProcessorRevision", WORD)]

#function references
VirtualQuery = WinDLL('kernel32',use_last_error=True).VirtualQueryEx
VirtualQuery.argtypes = [HANDLE,LPCVOID,POINTER(MEMORY_BASIC_INFORMATION),c_size_t]
VirtualQuery.restype = c_size_t

GetSystemInfo = WinDLL('kernel32',use_last_error=True).GetSystemInfo
GetSystemInfo.argtypes = [POINTER(SYSTEM_INFO)]
GetSystemInfo.restype = None

#obtain global system info
SI = SYSTEM_INFO ()
SI_pointer = byref (SI)
GetSystemInfo (SI_pointer)

def VirtualQueryEx(procHandle, address):
	MBI = MEMORY_BASIC_INFORMATION()
	MBI_pointer =  byref(MBI)
	length = sizeof(MBI)
	VirtualQuery(procHandle,address,MBI_pointer,length)
	return PyMEMORY_BASIC_INFORMATION(MBI)
	
def GetMemoryRegions(procHandle):
	region = VirtualQueryEx(procHandle, SI.MinimumApplicationAddress)
	memory_regions = []
	while region.BaseAddress != None:
		memory_regions.append(region)
		region = VirtualQueryEx(procHandle, region.BaseAddress+region.RegionSize)
	return memory_regions

def scan_page_int(procHandle, region, value):
	buffer = pymem.readBytes(procHandle,region.BaseAddress,region.RegionSize)
	length = len(buffer)
	address_list = []
	x = 0; y = 4
	while(y/4<length):
		if(buffer[x:y]!=b''):
			compare = struct.unpack("i",buffer[x:y])[0]
		if(compare == value):
			address_list.append(region.BaseAddress+x)
		x+=4
		y+=4
	return address_list
	
def scan_page_short(procHandle, region, value):
	buffer = pymem.readBytes(procHandle,region.BaseAddress,region.RegionSize)
	length = len(buffer)
	address_list = []
	x = 0; y = 2
	while(y/2<length):
		if(buffer[x:y]!=b''):
			compare = struct.unpack("h",buffer[x:y])[0]
		if(compare == value):
			address_list.append(region.BaseAddress+x)
		x+=2
		y+=2
	return address_list
	
def scan_page_byte(procHandle, region, value):
	buffer = pymem.readBytes(procHandle,region.BaseAddress,region.RegionSize)
	length = len(buffer)
	address_list = []
	x = 0; y = 1
	while(y<length):
		if(buffer[x:y]!=b''):
			compare = struct.unpack("b",buffer[x:y])[0]
		if(compare == value):
			address_list.append(region.BaseAddress+x)
		x+=1
		y+=1
	return address_list
	
def scan_page_float(procHandle, region, value):
	buffer = pymem.readBytes(procHandle,region.BaseAddress,region.RegionSize)
	length = len(buffer)
	address_list = []
	x = 0; y = 4
	while(y/4<length):
		if(buffer[x:y]!=b''):
			compare = struct.unpack("f",buffer[x:y])[0]
		if(compare == value):
			address_list.append(region.BaseAddress+x)
		x+=4
		y+=4
	return address_list
	
def scan_page_double(procHandle, region, value):
	buffer = pymem.readBytes(procHandle,region.BaseAddress,region.RegionSize)
	length = len(buffer)
	address_list = []
	x = 0; y = 8
	while(y/8<length):
		if(buffer[x:y]!=b''):
			compare = struct.unpack("d",buffer[x:y])[0]
		if(compare == value):
			address_list.append(region.BaseAddress+x)
		x+=8
		y+=8
	return address_list

def init_scan(procHandle, value, scan_type, memory_protection):
	regions = GetMemoryRegions(procHandle)
	addresses = []
	if(scan_type == type_int):
		for r in regions:
			if(r.Protect == memory_protection):
				addresses.extend(scan_page_int(procHandle,r,value))
		return addresses
	
	if(scan_type == type_short):
		for r in regions:
			if(r.Protect == memory_protection):
				addresses.extend(scan_page_short(procHandle,r,value))
		return addresses
	
	if(scan_type == type_byte):
		for r in regions:
			if(r.Protect == memory_protection):
				addresses.extend(scan_page_byte(procHandle,r,value))
		return addresses

	if(scan_type == type_float):
		for r in regions:
			if(r.Protect == memory_protection):
				addresses.extend(scan_page_float(procHandle,r,value))
		return addresses

	if(scan_type == type_double):
		for r in regions:
			if(r.Protect == memory_protection):
				addresses.extend(scan_page_double(procHandle,r,value))
		return addresses
	return None

def rescan_equals(procHandle, addresses, value, scan_type):
	new_addresses = []
	if(scan_type == type_int):
		for a in addresses:
			if(pymem.readInt(procHandle,a) == value):
				new_addresses.append(a)
		return new_addresses
	if(scan_type == type_short):
		for a in addresses:
			if(pymem.readShort(procHandle,a) == value):
				new_addresses.append(a)
		return new_addresses
	if(scan_type == type_byte):
		for a in addresses:
			if(pymem.readByte(procHandle,a) == value):
				new_addresses.append(a)
		return new_addresses
	if(scan_type == type_float):
		for a in addresses:
			if(pymem.readFloat(procHandle,a) == value):
				new_addresses.append(a)
		return new_addresses
	if(scan_type == type_double):
		for a in addresses:
			if(pymem.readDouble(procHandle,a) == value):
				new_addresses.append(a)
		return new_addresses
	return None

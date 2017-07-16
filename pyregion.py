"Module to interact with memory regions"

from ctypes import Structure, c_void_p, c_size_t, WinDLL, POINTER, byref, sizeof
from ctypes.wintypes import DWORD, HANDLE, LPCVOID

import pymem

class Region(Structure):
    """Structure for memory region information
    Contains:
    BaseAddress - A pointer to the base address of the region of pages.
    AllocationBase
    AllocationProtect
    RegionSize
    State
    Protect
    Type"""
    _fields_ = [
        ("BaseAddress", c_void_p),
        ("AllocationBase", c_void_p),
        ("AllocationProtect", DWORD),
        ("RegionSize", c_size_t),
        ("State", DWORD),
        ("Protect", DWORD),
        ("Type", DWORD)]

__VirtualQuery__ = WinDLL('kernel32', use_last_error=True).VirtualQueryEx
__VirtualQuery__.argtypes = [HANDLE, LPCVOID, POINTER(Region), c_size_t]
__VirtualQuery__.restype = c_size_t

# change this depending on your system's minimumApplicationAddress
# cannot use WinDLL('kernel32').GetSystemInfo - causes crash on exit
__min_address__ = 0x10000

def virtual_query_ex(process_handle, address):
    """Queries a process on a memory region - returns Region object

    Keyword arguments:
    process_handle --  handle to process
    address -- base address of the memory region
    """
    region = Region()
    __VirtualQuery__(process_handle, address, byref(region), sizeof(region))
    return region

def map_all_regions(process_handle):
    """Returns a list of all memory regions in a process

    Keyword arguments:
    process_handle -  handle to process"""
    regions = []
    current_address = __min_address__
    while True:
        current_region = virtual_query_ex(process_handle, current_address)
        if current_region.BaseAddress is None:
            break
        current_address = current_region.BaseAddress + current_region.RegionSize
        regions.append(current_region)
    return regions

def map_commit_regions(process_handle):
    "Returns a list of comittee memory regions in a process"
    regions = []
    current_address = __min_address__
    while True:
        current_region = virtual_query_ex(process_handle, current_address)
        if current_region.BaseAddress is None:
            break
        current_address = current_region.BaseAddress + current_region.RegionSize
        if current_region.State == 0x1000:
            regions.append(current_region)
    return regions

def dump_region(process_handle, region, file):
    "Dumps a single region into a file"
    buffer = pymem.read_bytes(process_handle, region.BaseAddress, region.RegionSize)
    with open(file, "rb") as current_file:
        current_file.write(buffer)

def dump_readable_memory(process_handle, file):
    "Dumps all readable memory in a process"
    regions = map_commit_regions(process_handle)
    with open(file, "wb") as current_file:
        for region in regions:
            buffer = pymem.read_bytes(process_handle, region.BaseAddress, region.RegionSize)
            current_file.write(buffer)

def find_bytes(process_handle, buffer):
    """Searches for a bytes-like object in process memory
    returns a list of addresses which matched at the time of scanning
    On a finding a match, skips the length of the match before searching for the next match

    Keyword arguments:
    process_handle -- handle to process
    buffer -- a bytes-like object; the bytes to scan for"""
    # gets a list of regions (filtered), scans each region for all matches
    regions = map_commit_regions(process_handle) # only get regions that are commited
    addresses = []
    for region in regions:
        if region.Type == 0x40000: # don't process mapped memory e.g. files, emulation
            continue
        remote_buffer = pymem.read_bytes(process_handle, region.BaseAddress, region.RegionSize)
        q_offset = 0
        while True:
            offset = remote_buffer.find(buffer, q_offset)
            if offset == -1:
                break
            else:
                addresses.append(region.BaseAddress + offset)
                q_offset = offset + len(buffer)
    return addresses

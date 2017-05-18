import pymem
from time import sleep
from threading import Thread
"""
Module for creating trainers for games or programs
Only attaches to a single process at a time
NOTE:
the type argument in Address.__init__ and Pointer.__init__ is a string
e.g 'int' or 'float' or 'byte'
"""
__author__ = "SamsonPianoFingers"
__credits__ = ["SamsonPianoFingers"]
__license__ = "GPL"
__version__ = "0.01"
__maintainer__ = "SamsonPianoFingers"
__email__ = "itsthatguyagain3@gmail.com"
__status__ = "Prototype"


process_handle = 0
sizeof_type = {'int': 4, 'short': 2, 'byte': 1, 'float': 4, 'double': 8}


def attach_process(process):
    """Attaches trainer to process

    Keyword arguments:
    process -- either process id or process name
    """
    global process_handle
    if(type(process) == int):
        process_handle = pymem.openProc(process)
    elif(type(process) == str):
        process_handle = pymem.openProcName(process)


def release_process():
    """Deattaches trainer from process"""
    global process_handle
    pymem.closeProc(process_handle)
    process_handle = 0


class Address():
    """Memory address class"""
    def __init__(self, address, type):
        """Address(address,type)
        
        Keyword arguments:
        address -- Location in the remote process's memory
        type -- a string representing variable type
        these are: 'byte', 'short', 'int, 'float, 'double'
        """
        self.address = address
        self.type = type
        self.size = sizeof_type.get(type)
        self.value = None
        self.lock_thread = None
        self.locked = False

    def __exit__(self, exc_type, exc_value, traceback):
        self.unlock()

    def read(self):
        """Reads and formats the data at self.address in remote process
        Returns the data that was read.
        """
        if(self.type == 'int'):
            self.value = pymem.readInt(process_handle, self.address)
        elif(self.type == 'short'):
            self.value = pymem.readShort(process_handle, self.address)
        elif(self.type == 'byte'):
            self.value = pymem.readByte(process_handle, self.address)
        elif(self.type == 'float'):
            self.value = pymem.readFloat(process_handle, self.address)
        elif(self.type == 'double'):
            self.value = pymem.readDouble(process_handle, self.address)
        return self.value

    def write(self, value):
        """Writes a value to self.address in remote process
        """
        if(self.type == 'int'):
            pymem.writeInt(process_handle, self.address, value)
        elif(self.type == 'short'):
            pymem.writeShort(process_handle, self.address, value)
        elif(self.type == 'byte'):
            pymem.writeByte(process_handle, self.address, value)
        elif(self.type == 'float'):
            pymem.writeFloat(process_handle, self.address, value)
        elif(self.type == 'double'):
            pymem.writeDouble(process_handle, self.address, value)

    def _lock_(self, value, interval=0.1):
        while self.locked is True:
            self.write(value)
            sleep(interval)

    def lock(self, value, interval=0.1):
        """Creates a thread which freezes self.address with specified value
        
        Keyword arguments:
        value -- value to freeze to
        (optional) interval -- freezing interval
        """
        if(self.locked is not True):
            self.locked = True
            self.lock_thread = Thread(
                target=self._lock_, args=([value, interval]))
            self.lock_thread.daemon = True
            self.lock_thread.start()

    def unlock(self):
        """Unfreezes self.address by killing the lock thread"""
        self.locked = False


class Pointer(Address):
    """Memory pointer class"""
    def __init__(self, base_address, offset_list, type):
        """Pointer(base_address, offset_list, type)
        
        Keyword arguments:
        base_address -- base address of pointer in remote process
        offset_list -- a list of offsets to follow when resolving
        type -- a string representing variable type that the pointer points to
        these are: 'byte', 'short', 'int, 'float, 'double'
        """
        super(Pointer, self).__init__(0, type)
        self.base_address = base_address
        self.offset_list = offset_list
        self.resolve()

    def resolve(self):
        """Resolves the pointer and caches it for read/write"""
        self.address = pymem.resolveMultiPointer(
            process_handle, self.base_address, self.offset_list)

    def resolve_and_read(self):
        """Resolves and reads the pointer. Also caches the pointer
        Returns the data that was read"""
        self.resolve()
        return self.read()

    def resolve_and_write(self, value):
        """Resolves and writes to pointer. Also caches the pointer
        
        Keyword arguments:
        value -- value to write to address pointed at by pointer"""
        self.resolve()
        self.write(value)

class Patch():
    """Memory patching class"""
    def __init__(self, address, patch_bytes):
        """Patch(address, patch_bytes)
        
        Keyword arguments:
        address -- address to patch
        patch_bytes -- bytes to change at self.address"""
        self.address = address
        self.patch_bytes = patch_bytes
        self.length = len(patch_bytes)
        self.original_bytes = pymem.readBytes(
            process_handle, self.address, self.length)

    def patch(self):
        """Applies patch to memory"""
        pymem.writeBytes(process_handle, self.address, self.patch_bytes)

    def restore_bytes(self):
        """Restores original bytes, removing the patch"""
        pymem.writeBytes(process_handle, self.address, self.original_bytes)

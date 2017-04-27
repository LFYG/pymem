import pymem
from time import sleep
from threading import Thread
process_handle = 0
sizeof_type = {'int':4, 'short':2, 'byte':1, 'float':4, 'double':8}

def set_process(process):
	global process_handle
	if(type(process) == int):
		process_handle = pymem.openProc(process)
	elif(type(process) == str):
		process_handle = pymem.openProcName(process)
	
def release_process():
	pymem.closeProc(process_handle)
	process_handle = 0

class Address():
	def __init__(self, address, type):
		self.address = address
		self.type = type
		self.size = sizeof_type.get(type)
		self.value = None
		self.lock_thread = None
		self.locked = False
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.unlock()
	
	def read(self):
		if(self.type == 'int'):
			self.value = pymem.readInt(process_handle, self.address)
		if(self.type == 'short'):
			self.value = pymem.readShort(process_handle, self.address)
		if(self.type == 'byte'):
			self.value = pymem.readByte(process_handle, self.address)
		if(self.type == 'float'):
			self.value = pymem.readFloat(process_handle, self.address)
		if(self.type == 'double'):
			self.value = pymem.readDouble(process_handle, self.address)
		return self.value
			
	def write(self, value):
		if(self.type == 'int'):
			pymem.writeInt(process_handle, self.address, value)
		if(self.type == 'short'):
			pymem.writeShort(process_handle, self.address, value)
		if(self.type == 'byte'):
			pymem.writeByte(process_handle, self.address, value)
		if(self.type == 'float'):
			pymem.writeFloat(process_handle, self.address, value)
		if(self.type == 'double'):
			pymem.writeDouble(process_handle, self.address, value)
			
	def _lock_(self, value, interval = 0.25):
		while self.locked==True:
			self.write(value)
			sleep(interval)

	def lock(self, value, interval = 0.25):
		if(self.locked!=True):
			self.locked=True
			self.lock_thread = Thread(target = _lock_, args = ([value,interval]) )
			self.lock_thread.start()
		
	def unlock(self):
		self.locked = False

class Pointer():
	def __init__(self, base_address, offset_list, type):
		self.base_address = base_address
		self.offset_list = offset_list
		self.type = type
		self.size = sizeof_type.get(type)
		self.resolved_address = 0
		self.resolve()
		self.lock_thread = None
		self.locked = False
		
	def __exit__(self, exc_type, exc_value, traceback):
		self.unlock()
	
	def resolve(self):
		self.resolved_address = pymem.resolveMultiPointer(process_handle, self.base_address, self.offset_list)
	
	def read(self):
		if(self.type == 'int'):
			self.value = pymem.readInt(process_handle, self.resolved_address)
		if(self.type == 'short'):
			self.value = pymem.readShort(process_handle, self.resolved_address)
		if(self.type == 'byte'):
			self.value = pymem.readByte(process_handle, self.resolved_address)
		if(self.type == 'float'):
			self.value = pymem.readFloat(process_handle, self.resolved_address)
		if(self.type == 'double'):
			self.value = pymem.readDouble(process_handle, self.resolved_address)
		
	def write(self, value):
		if(self.type == 'int'):
			pymem.writeInt(process_handle, self.resolved_address, value)
		if(self.type == 'short'):
			pymem.writeShort(process_handle, self.resolved_address, value)
		if(self.type == 'byte'):
			pymem.writeByte(process_handle, self.resolved_address, value)
		if(self.type == 'float'):
			pymem.writeFloat(process_handle, self.resolved_address, value)
		if(self.type == 'double'):
			pymem.writeDouble(process_handle, self.resolved_address, value)
	
	def resolve_and_read(self):
		self.resolve()
		self.read()
		
	def resolve_and_write(self, value):
		self.resolve()
		self.write(value)

	def _lock_(self, value, interval = 0.25):
		while self.locked==True:
			self.write(value)
			sleep(interval)

	def lock(self, value, interval = 0.25):
		if(self.locked!=True):
			self.locked=True
			self.lock_thread = Thread(target = self._lock_, args = ([value, interval]) )
			self.lock_thread.daemon = True
			self.lock_thread.start()
		
	def unlock(self):
		self.locked = False

class Patch():
	def __init__(self, address, patch_bytes):
		self.address = address
		self.patch_bytes = patch_bytes
		self.length = len(patch_bytes)
		self.original_bytes = pymem.readBytes(process_handle, self.address, self.length)
		
	def patch_bytes():
		pymem.writeBytes(process_handle, self.address, self.patch_bytes)
		
	def restore_bytes():
		pymem.writeBytes(process_handle, self.address, self.original_bytes)
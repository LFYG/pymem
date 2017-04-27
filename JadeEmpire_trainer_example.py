import pytrainer as pt
import keyboard
pt.set_process("JadeEmpire.exe")
base_ptr = 0x0076C924
#offsets = [0xA0, 0x0, 0x0, itemoffset]
class Player():
	def __init__(self):
		self.alignment = pt.Pointer(base_ptr, [0xA0,0,0,0x4E8], 'byte')
		self.maxhealth = pt.Pointer(base_ptr, [0xA0,0,0,0x948], 'int')
		self.maxchi = pt.Pointer(base_ptr, [0xA0,0,0,0x94C], 'int')
		self.maxfocus = pt.Pointer(base_ptr, [0xA0,0,0,0x488], 'float')
		
		self.x = pt.Pointer(base_ptr, [0xA0,0,0,0x44], 'float')
		self.y = pt.Pointer(base_ptr, [0xA0,0,0,0x48], 'float')
		self.z = pt.Pointer(base_ptr, [0xA0,0,0,0x4C], 'float')
		
		self.update()
		
	def update(self):
		self.alignment.resolve_and_read()
		self.maxhealth.resolve_and_read()
		self.maxchi.resolve_and_read()
		self.maxfocus.resolve_and_read()
		self.x.resolve_and_read()
		self.y.resolve_and_read()
		self.z.resolve_and_read()
		
	def set_open_palm(self):
		self.alignment.write(255)

	def set_closed_palm(self):
		self.alignment.write(0)
	
	def set_max_health(self,value):
		self.maxhealth.write(value)
		
	def set_max_chi(self,value):
		self.maxchi.write(value)

	def set_max_focus(self,value):
		self.maxfocus.write(value)
		
	def print_position(self):
		print(self.x.value, self.y.value, self.z.value)
	
	def writepos(self):
		self.x.write(self.x.value)
		self.y.write(self.y.value)
		self.z.write(self.z.value)
	
	def readpos(self):
		self.x.read()
		self.y.read()
		self.z.read()
		self.print_position()

player = Player()

player.set_open_palm()
player.set_max_health(5000)
player.set_max_chi(5000)
player.set_max_focus(5000)
#teleport hotkeys
keyboard.add_hotkey("r", self.readpos)
keyboard.add_hotkey("t", self.writepos)
import pymem
from time import sleep
jadeHandle = pymem.openProcName("JadeEmpire.exe")
#cheataddr section

#bases
baseptr = 0x0076C924
baseOffset = [0xA0,0x0,0x0]

#offsetLists
xOffset = baseOffset[:]
xOffset.append(0x44)

yOffset = baseOffset[:]
yOffset.append(0x48)

zOffset = baseOffset[:]
zOffset.append(0x4c)

camXOffset = baseOffset[:]
camXOffset.append(0x50)

camYOffset = baseOffset[:]
camYOffset.append(0x54)
#end cheataddr

#resolve ptr's
def resolvePtrs():
	x_p = pymem.resolveMultiPointer(jadeHandle, baseptr, xOffset)
	y_p = pymem.resolveMultiPointer(jadeHandle, baseptr, yOffset)
	z_p = pymem.resolveMultiPointer(jadeHandle, baseptr, zOffset)
	cx_p = pymem.resolveMultiPointer(jadeHandle, baseptr, camXOffset)
	cy_p = pymem.resolveMultiPointer(jadeHandle, baseptr, camYOffset)
	return (x_p,y_p,z_p,cx_p,cy_p)
#end

history = []
ptrs_list = resolvePtrs()
print("Recording player movement for 20 seconds")
for i in range(2000):
	x = pymem.readFloat(jadeHandle, ptrs_list[0])
	y = pymem.readFloat(jadeHandle, ptrs_list[1])
	z = pymem.readFloat(jadeHandle, ptrs_list[2])
	cx = pymem.readFloat(jadeHandle, ptrs_list[3])
	cy = pymem.readFloat(jadeHandle, ptrs_list[4])
	history.append((x,y,z,cx,cy))
	sleep(0.01)

print("Playing movement back")
for hist in reversed(history):
	pymem.writeFloat(jadeHandle, ptrs_list[0],hist[0])
	pymem.writeFloat(jadeHandle, ptrs_list[1],hist[1])	
	pymem.writeFloat(jadeHandle, ptrs_list[2],hist[2])
	pymem.writeFloat(jadeHandle, ptrs_list[3],hist[3])	
	pymem.writeFloat(jadeHandle, ptrs_list[4],hist[4])
	sleep(0.01)
instr="""
<x=0, y=4, z=0>
<x=-10, y=-6, z=-14>
<x=9, y=-16, z=-3>
<x=6, y=-1, z=2>
"""
# instr="""
# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
# """
instr="""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
import re

class Moon(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vx = 0
		self.vy = 0
		self.vz = 0

	def __str__(self):
		return "pos=<x=%3i, y=%3i, z=%3i>, vel=<x=%3i, y=%3i, z=%3i>" % (self.x, self.y, self.z, self.vx, self.vy, self.vz)
 
	def gravity(self, moons):
		for m in moons:
			if self == m: continue
			if self.x > m.x: self.vx -= 1
			elif self.x < m.x: self.vx += 1
			if self.y > m.y: self.vy -= 1
			elif self.y < m.y: self.vy += 1
			if self.z > m.z: self.vz -= 1
			elif self.z < m.z: self.vz += 1

	def velocity(self):
		self.x += self.vx
		self.y += self.vy
		self.z += self.vz

lines=instr.split("\n")
pat = "<x=(.*), y=(.*), z=(.*)>"
regex = re.compile(pat)
moons=[]
for l in lines:
	mat = re.match(regex, l)
	if mat:
		x, y, z = map(int, mat.group(1,2,3))
		moons.append(Moon(x, y, z))

for i in range(1001):
	print("After %i steps" % i)
	for m in moons:
		print(m)
	nrg = 0
	for m in moons:
		print((abs(m.x) + abs(m.y) + abs(m.z)))
		print((abs(m.vx) + abs(m.vy) + abs(m.vz)))
		nrg += (abs(m.x) + abs(m.y) + abs(m.z)) * (abs(m.vx) + abs(m.vy) + abs(m.vz))
	for m in moons:
		m.gravity(moons)
	for m in moons:
		m.velocity()

	print(nrg)
	
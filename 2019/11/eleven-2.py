import sys
import copy
instructions = open(sys.argv[1]).read()
# instructions = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
# instructions = "1102,34915192,34915192,7,4,7,99,0"
# instructions = "104,1125899906842624,99"
instructions = instructions.split(",")

class Intputer(object):
	(NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ, REL) = range(10)
	WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4, REL: 2}
	TERM = 99

	def __init__(self, instructions, inputs=[], id=""):
		self.program = list(map(int, instructions))
		self.saved_pc = 0
		self.saved_ram = copy.copy(self.program)
		self.saved_ram += [0] * 100000
		self.inputs = inputs
		self.last_output = None
		self.id = id
		self.relative_base = 0
		self.halted = False

	def get_a(self, modes, ram, pc):
		if modes[0] == 0:
			return ram[ram[pc+1]]
		elif modes[0] == 1:
			return ram[pc+1]
		elif modes[0] == 2:
			return ram[ram[pc+1]+self.relative_base]

	def get_a_addr(self, modes, ram, pc):
		if modes[0] == 0:
			return ram[pc+1]
		elif modes[0] == 1:
			# print("ERROR, INVALID IMMEDIATE MODE")
			return ram[pc+1]
		elif modes[0] == 2:
			return ram[pc+1]+self.relative_base

	def get_b(self, modes, ram, pc):
		# B is undefined, short circuit
		if len(modes) < 2: return None

		if modes[1] == 0:
			return ram[ram[pc+2]]
		elif modes[1] == 1:
			return ram[pc+2]
		elif modes[1] == 2:
			return ram[ram[pc+2]+self.relative_base]

	def get_c_addr(self, modes, ram, pc):
		# C is undefined, short circuit
		if len(modes) < 3: return None
		if modes[2] == 0:
			return ram[pc+3]
		elif modes[2] == 1:
			# print("ERROR, INVALID IMMEDIATE MODE")
			return ram[pc+3]
		elif modes[2] == 2:
			return ram[pc+3]+self.relative_base

	def out(self, *items):
		msg = ' '.join(map(str, items))
		if False:
			print(msg)

	def run(self):
		ram = self.saved_ram
		pc = self.saved_pc
		if self.saved_pc == -1:
			return
		while ram[pc] != self.TERM:
			opcode, modes = self.process_instruction(ram[pc])
			width = self.WIDTHS[opcode]
			a=self.get_a(modes, ram, pc)
			a_addr=self.get_a_addr(modes, ram, pc)
			b=self.get_b(modes, ram, pc)
			c_addr=self.get_c_addr(modes, ram, pc)
			self.out(ram[pc], ram[pc+1:pc+width])
			if opcode == self.ADD:
				self.out("ADD modes a b out", modes, a, b, a+b, "to", c_addr)
				ram[c_addr] = a + b
			elif opcode == self.MUL:
				self.out("MUL modes a b out", modes, a, b, a*b, "to", c_addr)
				ram[c_addr] = a * b
			elif opcode == self.INPUT:
				self.out("INPUT", modes, "to", a_addr)
				if self.inputs:
					in_val = self.inputs.pop()
					ram[a_addr] = in_val
				else:
					self.saved_pc = pc
					self.saved_ram = ram
					return self.INPUT, None

			elif opcode == self.OUTPUT:
				self.out("OUTPUT", modes, a)
				self.saved_pc = pc + self.WIDTHS[opcode]
				self.saved_ram = ram
				self.last_output = a
				return self.OUTPUT, self.last_output

			elif opcode == self.JTR:
				self.out("JTR", modes, a, "to", b)
				if a != 0: 
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.JFAL:
				self.out("JFAL", modes, a, "to", b)
				if a == 0:
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.LT:
				self.out("LT", modes, a, b)
				if a < b: 
					ram[c_addr] = 1
				else: 
					ram[c_addr] = 0
			elif opcode == self.EQ:
				self.out("EQ", modes, a, b)
				if a == b: 
					ram[c_addr] = 1
				else:
					ram[c_addr] = 0
			elif opcode == self.REL:
				self.out("REL", modes, a)
				self.relative_base += a
			elif opcode == self.NULL:
				print("ERROR: NULL INSTRUCTION")
			else: 
				print("ERROR: GARBAGE INSTRUCTION")
			pc += self.WIDTHS[opcode]

		self.saved_pc = -1
		self.saved_ram = ram
		self.halted = True
		return self.TERM, None

	def process_instruction(self, inst):
		opcode = int(str(inst)[-2:])
		modes = []
		for c in str(inst)[-3::-1]:
			modes.append(int(c))
		while len(modes) < self.WIDTHS[opcode] - 1:
			modes.append(0)
		return opcode, modes

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class Painter(object):

	def __init__(self):
		# 1 in input is for first white panel
		self.puter = Intputer(instructions, [1], id='a')
		self.loc = (0,0)
		self.dir = 0
		self.panels = {}
		self.trail = []

	def update(self, color, dir_delt):
		# print("PAINT", self.loc, color)
		self.trail.append(self.loc)
		self.panels[self.loc] = color
		self.dir = (self.dir + dir_delt) % 4
		delta = DIRS[self.dir]
		# print("TURN to", delta)
		self.loc = self.loc[0] + delta[0], self.loc[1] + delta[1]
		# print("MOVE to", self.loc)


	def run(self):
		outs = []

		while not self.puter.halted:
			code, out = self.puter.run()
			if code == Intputer.OUTPUT:
				outs.append(out)
				# print("OUTPUT", out)
				if len(outs) % 2 == 0:
					if outs[-1] == 1:
						dir_delt = 1
					else: dir_delt = -1
					color = outs[-2]
					# print("UPDATE", color, dir_delt)
					self.update(color, dir_delt)
			elif code == Intputer.INPUT: 
				# print("INPUT", self.panels.get(self.loc, 0))
				self.puter.inputs.append(self.panels.get(self.loc, 0))
			# print(self.trail)
		# print(outs)
		# print(len(self.panels.keys()))


painter = Painter()
painter.run()

from PIL import Image, ImageDraw

im = Image.new("1", (1000,1000))
center = (500, 500)
draw = ImageDraw.Draw(im)
for pt_k in painter.panels.keys():
	pt_color = painter.panels[pt_k]
	if pt_color == 1:
		draw.point(pt_k + center, fill="white")
		print(pt_k)

f = open("image.png", "wb")
# write to stdout
im.save(f, "PNG")
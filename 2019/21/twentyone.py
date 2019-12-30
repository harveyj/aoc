import sys
import copy
import random
instructions = open("twentyone-in.txt").read()
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
			print("ERROR")
			return None, -1
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
					in_val = self.inputs[0]
					self.inputs = self.inputs[1:]
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

class SpringDroid(object):

	def __init__(self, code):
		inputs = list(map(ord, code))
		print(inputs)
		self.puter = Intputer(instructions, inputs, id='a')
		self.outputs = []

	def run(self):
		for i in range(10000):
			code, out = self.puter.run()
			if code == Intputer.OUTPUT:
				# print("OUTPUT", out)
				self.outputs.append(out)
			elif code == Intputer.INPUT: 
				next_ip = raw_input()
				print("INPUT", next_ip)
				break
			else:
				# print("foo")
				break
		return self.outputs

prog = """
NOT H J
NOT E T
AND E J
NOT J J
NOT C T
AND T J
AND D J
NOT A T
OR T J
RUN
"""
# J = NOT (A AND B AND C)
prog = """
OR A J
AND B J
AND C J
NOT J J
OR E T
OR H T
AND T J
AND D J
NOT A T
OR T J
RUN
"""


prog = prog[1:]
sd = SpringDroid(prog)

out = sd.run()
for c in out:
	if c > 255:
		print(c)
	else: 
		print(chr(c), end='')
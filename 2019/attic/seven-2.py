#!/usr/bin/env python3

import sys
import copy
instructions = open(sys.argv[1]).read()
# instructions = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
# seq=[4,3,2,1,0]
# instructions = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
# seq=[0,1,2,3,4]
# instructions ="3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
# seq=[1,0,4,3,2]
instructions = instructions.split(",")

class Intputer(object):
	(NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ) = range(9)
	WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4}
	TERM = 99

	def __init__(self, instructions, inputs=[], id=""):
		self.program = list(map(int, instructions))
		self.saved_pc = 0
		self.saved_ram = copy.copy(self.program)
		self.saved_ram += [0] * 400
		self.inputs = inputs
		self.last_output = None
		self.id = id

	def run(self):
		ram = self.saved_ram
		pc = self.saved_pc
		if self.saved_pc == -1:
			return
		while ram[pc] != self.TERM:
			if ram[pc] == 0:
				print("INVALID OPCODE ", pc)
			opcode, modes = self.process_instruction(ram[pc])
			width = self.WIDTHS[opcode]
			a=0
			b=0
			c=0
			print(pc, ".", end="")
			if width > 2:
				a = ram[pc + 1] if modes[0] else ram[ram[pc + 1]] 
				b = ram[pc + 2] if modes[1] else ram[ram[pc + 2]] 
			if width > 3:
				c = ram[pc + 3] if modes[1] else ram[ram[pc + 3]] 

			if opcode == self.ADD:
				# print("ADD", modes, ram[pc+1], ram[pc+2], ram[pc+3])
				# print("ADD modes, a b out", modes, a, b, a+b, "to", c)
				ram[ram[pc + 3]] = a + b
			elif opcode == self.MUL:
				# print("MUL", modes, ram[pc+1], ram[pc+2], ram[pc+3])
				# print("MUL modes a b out", modes, a, b, a*b, "to", ram[pc+3])
				ram[ram[pc + 3]] = a * b
			elif opcode == self.INPUT:
				print("input ", self.id, self.inputs)
				if self.inputs:
					in_val = self.inputs.pop()
				else:
					self.saved_pc = pc
					self.saved_ram = ram
					return None
				# print("INPUT ", in_val, "to", ram[pc+1])

				ram[ram[pc + 1]] = in_val
			elif opcode == self.OUTPUT:
				# print("OUTPUT", modes, ram[pc+1])
				print("OUTPUT", ram[ram[pc + 1]])
				self.saved_pc = pc + self.WIDTHS[opcode]
				self.saved_ram = ram
				self.last_output = ram[ram[pc+1]]
				print("halt output")
				return self.last_output

			elif opcode == self.JTR:
				# print("JTR if", a, "to", b, ram[pc+1], "MODE" if modes[0] else "", )
				if a != 0: 
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.JFAL:
				# print("JFAL if", a, "to", b, ram[pc+1], "MODE" if modes[0] else "", )
				if a == 0:
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.LT:
				# print("LT", a, b)
				if a < b: 
					ram[ram[pc+3]] = 1
				else: 
					ram[ram[pc+3]] = 0
			elif opcode == self.EQ:
				# print("EQ", a, b)
				if a == b: 
					ram[ram[pc+3]] = 1
				else:
					ram[ram[pc+3]] = 0
			elif opcode == self.NULL:
				pass
			pc += self.WIDTHS[opcode]

		self.saved_pc = -1
		self.saved_ram = ram
		return None

	def process_instruction(self, inst):
		opcode = int(str(inst)[-2:])
		modes = []
		for c in str(inst)[-3::-1]:
			modes.append(int(c))
		while len(modes) < self.WIDTHS[opcode] - 1:
			modes.append(0)
		return opcode, modes

def chained_amplify(seq, a_in):
	intputers = [
		Intputer(instructions, [seq[0]], id='a'), Intputer(instructions, [seq[1]]),
		Intputer(instructions, [seq[2]]), Intputer(instructions, [seq[3]]), Intputer(instructions, [seq[4]])
		]

	next_input = a_in
	for i in range(1000000):
		idx = i % len(intputers)
		puter = intputers[idx]
		if next_input != None:
			# TODO: Use dequeue
			puter.inputs.insert(0, next_input)
			next_input = None
		next_input = puter.run()
		if sum([ip.saved_pc for ip in intputers]) == -5:
			break
	return intputers[4].last_output

# seq = [9, 8, 7, 6, 5]
# print(chained_amplify(seq, a_in=0))
the_max = 0
max_input = None
for a in range(5,10):
	for b in range(5,10):
		for c in range(5,10):
			for d in range(5,10):
				for e in range(5,10):
					seq=[a,b,c,d,e]
					# oh no.
					if a==b or a==c or a==d or a==e or b==c or b==d or b==e or c==d or c==e or d==e:
						continue
					out = chained_amplify(seq, a_in=0)
					if out > the_max:
						max_input = seq
						the_max = out

print(the_max, max_input)

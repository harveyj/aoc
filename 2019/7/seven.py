import sys
import copy
instring = open(sys.argv[1]).read()
instructions = instring.split(',')


class Intputer(object):
	(NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ) = range(9)
	WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4}
	TERM = 99

	def __init__(self, instring):
		self.program = list(map(int, instring))

	def run(self, inputs = []):
		ram = copy.copy(self.program)
		ram += [0] * 400
		pc = 0
		while ram[pc] != self.TERM:
			print(pc, ram[pc])
			opcode, modes = self.process_instruction(ram[pc])
			width = self.WIDTHS[opcode]
			a=0
			b=0
			if width > 2:
				a = ram[pc + 1] if modes[0] else ram[ram[pc + 1]] 
				b = ram[pc + 2] if modes[1] else ram[ram[pc + 2]] 

			if opcode == self.ADD:
				print("ADD", modes, ram[pc+1], ram[pc+2], ram[pc+3])
				print("ADD a b out", a, b, a+b)
				ram[ram[pc + 3]] = a + b
			elif opcode == self.MUL:
				print("MUL", modes, ram[pc+1], ram[pc+2], ram[pc+3])
				print("MUL a b out", a, b, a*b)
				ram[ram[pc + 3]] = a * b
			elif opcode == self.INPUT:
				print("INPUT", modes, ram[pc+1])
				if inputs:
					in_val = inputs.pop()
				else:
					in_val = int(input('input'))
				ram[ram[pc + 1]] = in_val
			elif opcode == self.OUTPUT:
				print("OUTPUT", modes, ram[pc+1])
				print("OUTPUT", ram[ram[pc + 1]])
			elif opcode == self.JTR:
				print("JTR", a)
				if a != 0: 
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.JFAL:
				print("JFAL", a)
				if a == 0:
					pc = b
					continue # needed because else pc gets incremented below
			elif opcode == self.LT:
				print("LT", a, b)
				if a < b: 
					ram[ram[pc+3]] = 1
				else: 
					ram[ram[pc+3]] = 0
			elif opcode == self.EQ:
				print("EQ", a, b)
				if a == b: 
					ram[ram[pc+3]] = 1
				else:
					ram[ram[pc+3]] = 0
			elif opcode == self.NULL:
				pass
			
			pc += self.WIDTHS[opcode]
		return ram

	def process_instruction(self, inst):
		opcode = int(str(inst)[-2:])
		# print('oc, inst', opcode, inst)
		modes = []
		# busted?
		for c in str(inst)[-3::-1]:
			modes.append(int(c))
		while len(modes) < self.WIDTHS[opcode] - 1:
			modes.append(0)
		return opcode, modes

Intputer(instructions).run(inputs=[1])

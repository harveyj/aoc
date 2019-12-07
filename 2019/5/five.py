import sys
instring = open(sys.argv[1]).read()
# instring = "1002,4,3,4,33"
# instring = "1101,100,-1,4,0"
# instring = "1101,100,-1,4,0"
# instring = "3,225,99"
# instring = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
# instring = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
instructions = instring.split(',')

(NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ) = range(9)
WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4}
TERM = 99

def run(instring):
	ram = list(map(int, instring))
	ram+=[0]*400
	pc = 0
	while ram[pc] != TERM:
		print(pc, ram[pc])
		opcode, modes = process_instruction(ram[pc])
		width = WIDTHS[opcode]
		a=0
		b=0
		if width > 2:
			a = ram[pc + 1] if modes[0] else ram[ram[pc + 1]] 
			b = ram[pc + 2] if modes[1] else ram[ram[pc + 2]] 

		if opcode == ADD:
			print("ADD", modes, ram[pc+1], ram[pc+2], ram[pc+3])
			print("ADD a b out", a, b, a+b)
			ram[ram[pc + 3]] = a + b
		elif opcode == MUL:
			print("MUL", modes, ram[pc+1], ram[pc+2], ram[pc+3])
			print("MUL a b out", a, b, a*b)
			ram[ram[pc + 3]] = a * b
		elif opcode == INPUT:
			print("INPUT", modes, ram[pc+1])
			in_val = int(input('input'))
			ram[ram[pc + 1]] = in_val
		elif opcode == OUTPUT:
			print("OUTPUT", modes, ram[pc+1])
			print("OUTPUT", ram[ram[pc + 1]])
		elif opcode == JTR:
			print("JTR", a)
			if a != 0: 
				pc = b
				continue # needed because else pc gets incremented below
		elif opcode == JFAL:
			print("JFAL", a)
			if a == 0:
				pc = b
				continue # needed because else pc gets incremented below
		elif opcode == LT:
			print("LT", a, b)
			if a < b: 
				ram[ram[pc+3]] = 1
			else: 
				ram[ram[pc+3]] = 0
		elif opcode == EQ:
			print("EQ", a, b)
			if a == b: 
				ram[ram[pc+3]] = 1
			else:
				ram[ram[pc+3]] = 0
		elif opcode == NULL:
			pass
		
		pc += WIDTHS[opcode]
	return ram

def process_instruction(inst):
	opcode = int(str(inst)[-2:])
	# print('oc, inst', opcode, inst)
	modes = []
	# busted?
	for c in str(inst)[-3::-1]:
		modes.append(int(c))
	while len(modes) < WIDTHS[opcode] - 1:
		modes.append(0)
	return opcode, modes

run(instructions)

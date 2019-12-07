import sys
instring = open(sys.argv[1]).read().split(',')

def run(a, b, instring):
	ram = map(int, instring)

	ram[1] = a
	ram[2] = b

	idx = 0
	while ram[idx] != 99:
		inst = ram[idx]
		print(inst)
		if inst == 1:
			ram[ram[idx + 3]] = ram[ram[idx + 1]] + ram[ram[idx+2]]
		elif inst == 2:
			ram[ram[idx + 3]] = ram[ram[idx + 1]] * ram[ram[idx+2]]

		idx += 4
	return ram

for a in range(1, 100):
	for b in range(1, 100):
		print(a, b, run(a, b, instring)[0])
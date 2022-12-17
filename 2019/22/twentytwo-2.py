import fileinput, itertools, collections

# VERY indebted to AoC reddit threads

instructions = [line.strip() for line in fileinput.input()]
# DECK_LENGTH = 10007
DECK_LENGTH = 119315717514047


# instr = """deal with increment 7
# deal into new stack
# deal into new stack"""
# instr = """deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack
# deal into new stack"""
# instr = """deal with increment 7"""
# instr = """cut 6
# deal with increment 7
# deal into new stack"""
# instr = """cut 6
# deal with increment 7"""
# instr = """deal with increment 3"""
# instr = """deal with increment 7
# deal with increment 9
# cut -2
# """
# instr = """deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1"""


# instructions = [line.strip() for line in instr.split('\n')]
# DECK_LENGTH = 10


def new_one_iter():
	a = 1
	b = 0
	for l in instructions:
		if l == "deal into new stack":
			b -= a
			a *= -1
		elif "deal with increment" in l:
			n = int(l.split()[-1])
			a *= pow(int(n), -1, DECK_LENGTH)
		elif "cut" in l:
			n = int(l.split()[-1])
			b += a*n
	return (a, b)


# def rev_one_iter(index):
# 	for l in instructions[::-1]:
# 		# print(index)
# 		# print(l)
# 		if l == "deal into new stack":
# 			index = rev_deal_into(index)
# 		elif "deal with increment" in l:
# 			n = int(l.split()[-1])
# 			index = rev_increment(index, n)
# 		elif "cut" in l:
# 			n = int(l.split()[-1])
# 			index = rev_cut(index, n)
# 	return index

a, b = new_one_iter()    
all_a  = pow(a, 101741582076661, DECK_LENGTH)
all_b  = b * (1 - pow(a, 101741582076661, DECK_LENGTH)) * pow(1 - a, -1, DECK_LENGTH)    

print((2020 * all_a + all_b) % DECK_LENGTH)

# for i in range(DECK_LENGTH):
# 	print("into", i, deal_into(i))
# for i in range(DECK_LENGTH):
# 	print("cut", i, cut(i, 3))
# for i in range(DECK_LENGTH):
# 	print("inc", i, increment(i, 3))

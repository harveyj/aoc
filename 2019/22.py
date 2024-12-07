#! /usr/bin/env python3

import puzzle
import fileinput, itertools, collections

# instr = """deal with increment 7
# deal into new stack
# deal into new stack"""
# instr = """cut 6
# deal with increment 7
# deal into new stack
# """
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


def deal_into(deck):
	deck.reverse()
	return deck

def cut(deck, n):
	return deck[n:] + deck[:n]

def increment(deck, n, DECK_LENGTH):
	new_deck = [0] * DECK_LENGTH
	for i in range(DECK_LENGTH):
		j = (i*n) % DECK_LENGTH
		new_deck[j] = deck[i]
		# print(i, j, (-i * n))
	return new_deck

def one_iter(deck, instructions, DECK_LENGTH):
	for l in instructions:
		if l == "deal into new stack":
			deck = deal_into(deck)
		elif "deal with increment" in l:
			n = int(l.split()[-1])
			deck = increment(deck, n, DECK_LENGTH)
		elif "cut" in l:
			n = int(l.split()[-1])
			deck = cut(deck, n)
	return deck

def new_one_iter(instructions, DECK_LENGTH):
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


def one(INPUT):
	DECK_LENGTH = 10007
	instructions = [line.strip() for line in INPUT]
	my_deck = list(range(DECK_LENGTH))
	my_deck = one_iter(my_deck, instructions, DECK_LENGTH)
	return my_deck.index(2019)

# VERY indebted to AoC reddit threads
def two(INPUT):
	DECK_LENGTH = 119315717514047
	instructions = [line.strip() for line in INPUT]
	a, b = new_one_iter(instructions, DECK_LENGTH)    
	all_a  = pow(a, 101741582076661, DECK_LENGTH)
	all_b  = b * (1 - pow(a, 101741582076661, DECK_LENGTH)) * pow(1 - a, -1, DECK_LENGTH)    
	return (2020 * all_a + all_b) % DECK_LENGTH

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "22")

  p.run(one, 0)
  p.run(two, 0)

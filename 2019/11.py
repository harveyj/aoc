#!/usr/bin/env python3
import puzzle, re
from intputer import Intputer

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class Painter(object):

	def __init__(self, instructions):
		self.puter = Intputer(instructions, [1], id='a', user_input=False)
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
				print("OUTPUT", out)
				if len(outs) % 2 == 0:
					if outs[-1] == 1:
						dir_delt = 1
					else: dir_delt = -1
					color = outs[-2]
					print("UPDATE", color, dir_delt)
					self.update(color, dir_delt)
			elif code == Intputer.INPUT: 
				print("INPUT", self.panels.get(self.loc, 0))
				self.puter.inputs.append(self.panels.get(self.loc, 0))
			# print(self.trail)
		# print(outs)
		print(len(self.panels.keys()))



def one(INPUT):
  Painter(INPUT[0].split(',')).run()
  out = 0
  return out

def two(INPUT):
  invals = parse_input()
  out = 0
  return out

p = puzzle.Puzzle("2019", "11")
p.run(one, 0)
# p.run(two, 0)

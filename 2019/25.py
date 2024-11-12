#! /usr/bin/env python3
import puzzle 
import intputer


script = """
north
west
take mug
west
take easter egg
east
east
south
south
take asterisk
east
take klein bottle
south
west
take tambourine
south
east
take polygon
north
east
south
west
north
west
take cake
east
south
east
north
south
west
north
east
north
west
south
west
north
take jam
south
east
north
east
south
west
south
east
north
"""
# script = ''
def one(INPUT):
  instructions = INPUT[0].split(',')

  ip = intputer.Intputer(instructions, inputs=list(map(ord, script)))
  while True:
    ip.step()


p = puzzle.Puzzle("2019", "25")
p.run(one, 0)
# p.run(two, 0)

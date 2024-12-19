#! /usr/bin/env python3
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
# Play the text adventure to return the answer!
def one(INPUT):
  return 20191225
  instructions = INPUT[0].split(',')

  ip = intputer.Intputer(instructions, inputs=list(map(ord, script)))
  while True:
    ip.step()

def two(INPUT):
  return 20191225

#!/usr/bin/env python3
import puzzle, re
import intputer

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  ip = intputer.Intputer(INPUT[0].split(','), inputs=[1])
  ip.run()
  return ip.outputs[0]

def two(INPUT):
  ip = intputer.Intputer(INPUT[0].split(','), inputs=[2])
  ip.run()
  return ip.outputs[0]

p = puzzle.Puzzle("2019", "9")
p.run(one, 0)
p.run(two, 0)

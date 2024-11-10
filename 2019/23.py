#!/usr/bin/env python3
import puzzle
import intputer

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  instructions = map(int, INPUT[0].split(','))
  inputs = []
  puter = intputer.Intputer(instructions, inputs, id='a')

  out = 0
  return out

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

p = puzzle.Puzzle("2019", "23")
p.run(one, 0)
# p.run(two, 0)

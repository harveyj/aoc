#!/usr/bin/env python3
import puzzle, library
import re

def parse(INPUT):
  for l in INPUT:
    yield int(l)


def one(INPUT):
  insts = list(parse(INPUT))
  pc = 0; steps = 0
  while True:
    steps += 1
    insts[pc] += 1
    pc += insts[pc] - 1 # back out the += 1 above
    if not 0 <= pc < len(insts):
      print('terminate')
      return steps

def two(INPUT):
  insts = list(parse(INPUT))
  pc = 0; steps = 0
  while True:
    steps += 1
    new_pc = pc + insts[pc]
    if insts[pc] > 2:
      insts[pc] -= 1
    else:
      insts[pc] += 1
    pc = new_pc
    if not 0 <= pc < len(insts):
      print('terminate')
      return steps

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "5")

  p.run(one, 0)
  p.run(two, 0)

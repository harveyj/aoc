#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict
import copy

def exec(op, a, b, c, regs):
  new_regs = copy.copy(regs)
  a = a if op in ['GTIR', 'SETI', 'EQIR'] else regs[a]
  b = b if op in ['ADDI', 'MULI', 'BANI', 'BORI', 'GTRI', 'EQRI'] else regs[b]
  if op in ['ADDR', 'ADDI']:
    new_regs[c] = a + b
  elif op in ['MULR', 'MULI']:
    new_regs[c] = a * b
  elif op in ['BANR', 'BANI']:
    new_regs[c] = a & b
  elif op in ['BORR', 'BORI']:
    new_regs[c] = a | b
  elif op in ['SETR', 'SETI']:
    new_regs[c] = a
  elif op in ['GTIR', 'GTRI', 'GTRR']:
    new_regs[c] = 1 if a > b else 0
  elif op in ['EQIR', 'EQRI', 'EQRR']:
    new_regs[c] = 1 if a == b else 0
  return new_regs

def one(INPUT):
  regs = defaultdict(int)
  pc_addr = int(INPUT[0].split()[1])
  instrs = [(l.split()[0], *library.ints(l)) for l in INPUT[1:]]
  pc = 0
  while True:
    regs[pc_addr] = pc
    if pc >= len(instrs): break
    op, a, b, c = instrs[pc]
    op = op.upper()
    regs = exec(op, a, b, c, regs)
    pc = regs[pc_addr]
    pc += 1
  return regs[0]

def two(INPUT):
  # Decompile the program. The program computes a number and then returns the sum of all factors of that number.
  # First, run the program to get the number. Not necessary to get the output for my input, but lets us run against arbitrary inputs.
  regs = defaultdict(int)
  regs[0] = 1
  pc_addr = int(INPUT[0].split()[1])
  instrs = [(l.split()[0], *library.ints(l)) for l in INPUT[1:]]
  pc = 0
  while True:
    regs[pc_addr] = pc
    if pc >= len(instrs): break
    op, a, b, c = instrs[pc]
    op = op.upper()
    old_regs = regs
    regs = exec(op, a, b, c, regs)
    pc = regs[pc_addr]
    pc += 1
    # The breakpoint that breaks when the number is set into register 3.
    if regs[3] != old_regs[3] and regs[3] > 10000:
      break

  num = regs[3]
  # Compute the sum of all factors
  return sum([i for i in range(1,num+1) if num / i == num // i])

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "19")
  print(p.run(one, 0))
  print(p.run(two, 0))
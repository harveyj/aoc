#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx
import itertools
import copy

def parse_input(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  tests, prog = chunks[:-1], chunks[-1]
  for chunk in tests:
    chunk = chunk.split('\n')
    before, instr, after = library.ints(chunk[0]), library.ints(chunk[1]), library.ints(chunk[2])
    yield before, instr, after

def get_prog(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  _, prog = chunks[:-1], chunks[-1]
  return map(library.ints, prog.split('\n'))

ADDR, ADDI, MULR, MULI, BANR, BANI, BORR, BORI, SETR, SETI,GTIR,GTRI,GTRR,EQIR,EQRI,EQRR = range(16,32)
ops = [ADDR, ADDI, MULR, MULI, BANR, BANI, BORR, BORI, SETR, SETI,GTIR,GTRI,GTRR,EQIR,EQRI,EQRR]
op_names = 'ADDR,ADDI,MULR,MULI,BANR,BANI,BORR,BORI,SETR,SETI,GTIR,GTRI,GTRR,EQIR,EQRI,EQRR'.split(',')
def exec(op, a, b, c, regs):
  new_regs = copy.copy(regs)
  a = a if op in [GTIR, SETI, EQIR] else regs[a]
  b = b if op in [ADDI, MULI, BANI, BORI, GTRI, EQRI] else regs[b]
  if op in [ADDR, ADDI]:
    new_regs[c] = a + b
  elif op in [MULR, MULI]:
    new_regs[c] = a * b
  elif op in [BANR, BANI]:
    new_regs[c] = a & b
  elif op in [BORR, BORI]:
    new_regs[c] = a | b
  elif op in [SETR, SETI]:
    new_regs[c] = a
  elif op in [GTIR, GTRI, GTRR]:
    new_regs[c] = 1 if a > b else 0
  elif op in [EQIR, EQRI, EQRR]:
    new_regs[c] = 1 if a == b else 0
  return new_regs

def one(INPUT):
  tests = parse_input(INPUT)
  tot = 0
  for before, instr, after in tests:
    op_num, a, b, c = instr
    possible = set()
    for op in ops:
      result = exec(op, a, b, c, before)
      if result == after:
        possible.add(op)
    if len(possible) > 2: tot += 1
  return tot

def two(INPUT):
  tests = parse_input(INPUT)
  # Key: each canonical opcode (16-31). Value: Possible candidates it could be.
  possibles = {op_code: list(range(16)) for op_code in ops}
  for before, instr, after in tests:
    op_num, a, b, c = instr
    for op in ops:
      result = exec(op, a, b, c, before)
      if result == after:
        pass
      else:
        if op_num in possibles[op]:
          possibles[op].remove(op_num)
  correct = dict()
  while True:
    for opcode, op_possibles in possibles.items():
      if len(op_possibles) == 1:
        only_possible = op_possibles[0]
        correct[opcode] = only_possible
        for other_op in [k for k in possibles.keys() if k != opcode]:
          if only_possible in possibles[other_op]:
            possibles[other_op].remove(only_possible)
    if len(correct) == 16: break
  op_lookup = {possibles[key][0]: key for key in possibles}

  regs = [0,0,0,0]
  for instr in get_prog(INPUT):
    op_num, a, b, c = instr
    op = op_lookup[op_num]
    regs = exec(op, a, b, c, regs)
    print(regs)
  return regs[0]

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "16")
  print(p.run(one, 0))
  print(p.run(two, 0))
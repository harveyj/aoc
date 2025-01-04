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
  # Sort of a hack, but hey. Poke around in the assembly, figure out that at line 28 we do the
  # equality check that leads to terminate. Break at that point, read off register five. r0 has to
  # be equal to it, so r0 is the answer. Confirm bc r0 is not touched elsewhere in the program
  bkpt = [28]
  fives = set()
  while True:
    regs[pc_addr] = pc
    if pc >= len(instrs): break
    op, a, b, c = instrs[pc]
    op = op.upper()
    old_regs = regs
    regs = exec(op, a, b, c, regs)
    if pc in bkpt: 
      fives.add(regs[5])
      break
    pc = regs[pc_addr]
    pc += 1
  return regs[5]

def two(INPUT):
  # Translate the core of the assembler to python, loop through it really fast. 
  def nxt(prev):
    regs = [0,0,0,0,0,0]
    regs[4] = prev | 65536
    regs[5] = 13159625
    for i in range(3):
      regs[3] = regs[4] & 255
      regs[5] += regs[3]
      regs[5] &= 16777215
      regs[5] *= 65899
      regs[5] &= 16777215
      if regs[4] > 256: regs[4] //= 256
    return regs[5]
  seen = set()
  num = one(INPUT)
  last = 0
  while True:
    seen.add(num)
    num = nxt(num)
    if num in seen: return last
    last = num


if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "21")
  print(p.run(one, 0))
  print(p.run(two, 0))
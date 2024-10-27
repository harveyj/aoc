#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib
from collections import defaultdict

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT:
    yield re.match(pat, l).groups()

# snd X plays a sound with a frequency equal to the value of X.
# set X Y sets register X to the value of Y.
# add X Y increases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
# mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
# rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
# jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

def rewrite_1(xy, regs):
  new_xy = xy[:1]
  for val in xy[1:]:
    if val in regs:
      new_xy.append(regs[val])
    else: new_xy.append(int(val))
  return new_xy

def rewrite_2(xy, regs):
  new_xy = []
  for val in xy:
    if val in regs:
      new_xy.append(regs[val])
    else: 
      new_xy.append(int(val))
  return new_xy

def rewrite_3(xy, regs):
  return [regs[xy[0]], None]

def one(INPUT):
  instrs = INPUT
  regs = defaultdict(int)
  snd = None
  rcv = None
  pc = 0
  while True:
    inst = instrs[pc]
    op, xy = inst.split()[0], inst.split()[1:]
    if op in ['snd', 'rcv']:
      x, y = rewrite_3(xy, regs)
    elif op in ['jgz']:
      x, y = rewrite_2(xy, regs)
    else:
      x, y = rewrite_1(xy, regs)

    if op == 'snd':
      snd = x
    elif op == 'set':
      regs[x] = y
    elif op == 'add':
      new = regs[x] + y
      regs[x] = new
    elif op == 'mul':
      new = regs[x] * y
      regs[x] = new
    elif op == 'mod':
      new = regs[x] % y
      regs[x] = new
    elif op == 'rcv':
      if x != 0:
        rcv = snd
        return rcv
    elif op == 'jgz':
      if x > 0:
        # cancel out the += 1 at the end of the loop
        pc += y -1
    pc += 1

def two(INPUT):
  return 0

p = puzzle.Puzzle("2017", "18")
p.run(one, 1)
p.run(two, 0)

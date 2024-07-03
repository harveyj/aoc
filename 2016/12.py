#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import collections


def parse(INPUT):
  pat = re.compile('(\w+) (\w+) ?([-]?\w+)?')
  for l in INPUT:
    if not re.match(pat, l):
      print('PARSE ERROR:', l)
    yield re.match(pat, l).groups()


def one(INPUT, two=True):
  pc = 0; regs = collections.defaultdict(int)
  instrs = list(parse(INPUT))
  while pc < len(instrs):
    # print(instrs[pc])
    inst = instrs[pc]
    op = inst[0]
    if op == 'cpy':
      if inst[1] in 'abcd':
        regs[inst[2]] = regs[inst[1]]
      else:
        regs[inst[2]] = int(inst[1])
      pc += 1
    elif op == 'inc':
      regs[inst[1]] += 1
      pc += 1
    elif op == 'dec':
      regs[inst[1]] -= 1
      pc += 1
    elif op == 'jnz':
      if inst[1].isdecimal(): # handle literal value
        if int(inst[1]) != 0:
          pc += eval(inst[2])
      elif regs[inst[1]] != 0:
        pc += eval(inst[2])
      else: pc += 1
  print(regs)
  return 0

def two(INPUT):
  return 0

p = puzzle.Puzzle("12")
p.run(one, 1)

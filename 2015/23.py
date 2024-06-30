#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import collections


def parse(INPUT):
  pat = re.compile('(\w+) ([+-]?\w+)?(, [+-]\d+)?')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()


def onetwo(INPUT, two=True):
  pc = 0; regs = collections.defaultdict(int)
  if two:
    regs['a'] = 1
  instrs = list(parse(INPUT))
  while pc < len(instrs):
    inst = instrs[pc]
    op = inst[0]
    if op == 'hlf':
      regs[inst[1]] /= 2
      pc += 1
    elif op == 'tpl':
      regs[inst[1]] *= 3
      pc += 1
    elif op == 'inc':
      regs[inst[1]] += 1
      pc += 1
    elif op == 'jmp':
      pc += eval(inst[1])
    elif op == 'jie':
      pc += 1 if regs[inst[1]] % 2 == 1 else eval(inst[2][1:])
    elif op == 'jio':
      pc += 1 if regs[inst[1]] != 1 else eval(inst[2][1:])
  print(regs)
  return 0

def two(INPUT):
  return 0

p = puzzle.Puzzle("23")
p.run(onetwo, 0)

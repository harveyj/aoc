#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import collections
import copy, math

def parse(INPUT):
  pat = re.compile(r'(\w+) ([-]?\w+) ?([-]?\w+)?')
  for l in INPUT:
    # print(l)
    if not re.match(pat, l):
      print('PARSE ERROR:', l)
    yield list(re.match(pat, l).groups())

def convert(str_val):
  try:
    return int(str_val)
  except ValueError:
    return None

def run(instrs, regs, watch=[], pc=0):
  last = copy.copy(regs)
  while pc < len(instrs):
    inst = instrs[pc]
    op = inst[0]
    if op == 'cpy':
      if inst[2].isdigit():
        continue
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
      value = convert(inst[2])
      if not value: value = regs[inst[2]]
      if inst[1].isdecimal(): # handle literal value
        if int(inst[1]) != 0:
          pc += value
      elif regs[inst[1]] != 0:
        pc += value
      else: pc += 1
    elif op == 'tgl':
      # print('.', pc, inst, regs)
      print('TOGGLE')
      if inst[1].isdecimal(): # handle literal value
        tgt = pc + eval(inst[1])
      elif regs[inst[1]] != 0:
        tgt = pc + regs[inst[1]]
      if tgt >= len(instrs):
        pc += 1
        continue
      tgt_op = instrs[tgt]
      if not tgt_op[2]:
        if tgt_op[0] == 'inc':
          tgt_op[0] = 'dec'
        else:
          tgt_op[0] = 'inc'
      else:
        if tgt_op[0] == 'jnz':
          tgt_op[0] = 'cpy'
        else:
          tgt_op[0] = 'jnz'
      pc += 1
    for reg in watch:
      if last[reg] != regs[reg]:
        print(f'{last[reg]}==>{regs[reg]}')
        last[reg] = regs[reg]
        return regs, pc, instrs
  return regs

def one(INPUT):
  regs = collections.defaultdict(int)
  regs['a'] = 7
  instrs = list(parse(INPUT))
  regs = run(instrs, regs)
  return regs['a']

def two(INPUT):
  regs = collections.defaultdict(int)
  regs['a'] = 12
  instrs = list(parse(INPUT)) 
  regs, pc, instrs = run(instrs, regs, watch=['b'], pc=0)
  regs, pc, instrs = run(instrs, regs, watch=['b'], pc=pc)
  regs, pc, instrs = run(instrs, regs, watch=['b'], pc=pc)
  print(regs, pc)
  # mild cheat - extracted from code
  return regs['a'] * math.factorial(regs['b']) + 95*73

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "23")
  print(p.run(one, 0))
  print(p.run(two, 0))
  
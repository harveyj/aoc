#!/usr/bin/env python3
import puzzle
import re
import collections

def parse(INPUT):
  pat = re.compile(r'(\w+) ([-]?\w+) ?([-]?\w+)?')
  for l in INPUT:
    if not re.match(pat, l):
      print('PARSE ERROR:', l)
    yield list(re.match(pat, l).groups())

def resolve(val, regs):
  if val.lstrip("-").isdigit():
    return int(val)
  return regs[val]

def evaluate(INPUT, a_val, max_instr=None, bkpt=-1):
  pc = 0; regs = {'a':0, 'b':0, 'c':0, 'd':0}
  regs['a'] = a_val
  instrs = list(parse(INPUT))
  total = 0
  outs = []
  while pc < len(instrs):
    total += 1
    if total == max_instr:
      break
    # print(instrs[pc])
    inst = instrs[pc]
    op = inst[0]
    if pc+1 == bkpt:
      print(pc, inst, regs)
      input()
      # return regs
    if op == 'cpy':
      val_1 = resolve(inst[1], regs)
      regs[inst[2]] = val_1
      pc += 1
    elif op == 'inc':
      regs[inst[1]] += 1
      pc += 1
    elif op == 'dec':
      regs[inst[1]] -= 1
      pc += 1
    elif op == 'jnz':
      value_1 = resolve(inst[1], regs)
      value_2 = resolve(inst[2], regs)
      if value_1 != 0: 
        pc += value_2
      else: 
        pc += 1
    elif op == 'out':
      value = resolve(inst[1], regs)
      if value == None: value = regs[inst[1]]
      outs.append(value)
      pc += 1
  return regs, outs

def one(INPUT):
  for a_val in range(0, 200):
    regs, outs = evaluate(INPUT, a_val, max_instr=50000, bkpt=-1)
    if outs[:10] == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
      return a_val


def two(INPUT):
  print('Merry Christmas!')
  return 20161225

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "25")
  p.run(one, 0)
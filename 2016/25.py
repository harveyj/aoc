#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import collections


def parse(INPUT):
  pat = re.compile('(\w+) ([-]?\w+) ?([-]?\w+)?')
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


def evaluate(INPUT, a_val, max_instr=None):
  pc = 0; regs = collections.defaultdict(int)
  regs['a'] = a_val
  instrs = list(parse(INPUT))
  total = 0
  while pc < len(instrs):
    total += 1
    print(regs)
    # if pc == 9:
      # input()
      # print('.', end='')
    if total == max_instr:
      # for r in regs: print(r, regs[r])
      # for i in instrs: print(i)
      print('done')
      break
    # print(instrs[pc])
    inst = instrs[pc]
    op = inst[0]
    # print(pc, inst, regs)
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
      print('.', pc, inst, regs)
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
    elif op == 'out':
      value = convert(inst[2])
      if not value: value = regs[inst[2]]
      print('OUT ', value)
  return 0

def one(INPUT):
  for a_val in range(0, 3000):
    print(a_val)
    evaluate(INPUT, a_val, max_instr=100000)
    input()
# did this by hand in a spreadsheet due to extensive disassembly

def two(INPUT):
  print('Merry Christmas!')
  return 20161225

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "25")
  p.run(one, 0)
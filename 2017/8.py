#!/usr/bin/env python3
import puzzle
import re
from collections import defaultdict

def parse(INPUT):
  pat = re.compile('(\w+) (\w+) (-?\d+) if (.*)')
  for l in INPUT:
    # print(l)
    yield re.match(pat, l).groups()


def onetwo(INPUT):
  regs = defaultdict(int)
  max_val = 0
  for l in parse(INPUT):
    reg, op, val, pred = l
    val = int(val)
    reg_2 = pred.split()[0]
    pred = re.sub('(\w+)', f'regs["{reg_2}"]', pred, 1)
    if eval(pred):
      if op == 'inc':
        regs[reg] += val
      else: 
        regs[reg] -= val
    if regs[reg] > max_val:
      max_val = regs[reg]
  return max(regs.values()), max_val

p = puzzle.Puzzle("2017", "8")
p.run(onetwo, 0)

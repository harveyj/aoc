#!/usr/bin/env python3
import puzzle
import re
from library import Grid

def parse(INPUT):
  instrs = []
  for l in INPUT:
    if 'toggle' in l:
      instr = ['toggle']
    elif 'turn on' in l:
      instr = ['turn on']
    else:
      instr = ['turn off']
    match = re.findall('(\d+)', l)

    for m in match:
      instr.append(int(m))
    instrs.append(instr)
  return instrs

def one(INPUT):
  G = Grid(1000, 1000)
  instrs = parse(INPUT)
  for (op, x1, y1, x2, y2) in instrs:
    for x in range(x1, x2 + 1):
      for y in range(y1, y2 + 1):
        if op == 'toggle': 
          tgt = '#' if (G.get((x, y)).strip() == '.') else '.'
          G.set((x, y), tgt)
        elif op == 'turn on': G.set((x, y), '#')
        elif op == 'turn off': G.set((x, y), '.')
  return len(G.detect('#'))

def two(INPUT):
  instrs = parse(INPUT)
  G = Grid(1000, 1000)
  for x in range(0, 1000):
    for y in range(0, 1000):
      G.set((x, y), 0)
  for (op, x1, y1, x2, y2) in instrs:
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        if op == 'toggle': G.set((x, y), G.get((x, y), 0) + 2)
        elif op == 'turn on': G.set((x, y), G.get((x, y), 0) + 1)
        elif op == 'turn off': G.set((x, y), max(0, G.get((x, y), 0) - 1))
  tot = 0
  for x in range(0, 1000):
    for y in range(0, 1000):
      tot += G.get((x, y))
  return tot

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "6")

  p.run(one, 0)
  p.run(two, 0)

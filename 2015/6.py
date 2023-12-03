#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
from library import Grid

def parse(INPUT):
  instrs = []
  for l in INPUT.split('\n'):
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
  instrs = parse(INPUT)
  G = Grid(False, 1000, 1000)
  print(instrs)
  for (op, x1, y1, x2, y2) in instrs:
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        if op == 'toggle': G.set((x, y), not G.get((x, y)))
        elif op == 'turn on': G.set((x, y), True)
        elif op == 'turn off': G.set((x, y), False)
  on = 0
  for x in range(0, 1000):
    for y in range(0, 1000):
      if G.get((x, y)): on +=1
  return on

def two(INPUT):
  instrs = parse(INPUT)
  G = Grid(0, 1000, 1000)
  for (op, x1, y1, x2, y2) in instrs:
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        if op == 'toggle': G.set((x, y), G.get((x, y)) + 2)
        elif op == 'turn on': G.set((x, y), G.get((x, y)) + 1)
        elif op == 'turn off': G.set((x, y), max(0, G.get((x, y)) - 1))
  tot = 0
  for x in range(0, 1000):
    for y in range(0, 1000):
      tot += G.get((x, y))
  return tot

p = puzzle.Puzzle("6")
# p.run(one, 0)
p.run(two, 0)

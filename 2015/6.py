#!/usr/bin/env python3
import puzzle
import re
from library import Grid
from rtree import index
import numpy

def parse(INPUT):
  instrs = []
  for l in INPUT:
    if 'toggle' in l:
      instr = ['toggle']
    elif 'turn on' in l:
      instr = ['turn on']
    else:
      instr = ['turn off']
    match = re.findall(r'(\d+)', l)

    for m in match:
      instr.append(int(m))
    instrs.append(instr)
  return instrs

def one(INPUT):
  G = numpy.zeros((1000, 1000), dtype=numpy.bool)
  instrs = parse(INPUT)
  for (op, x1, y1, x2, y2) in instrs:
    if op == 'toggle': 
      G[x1:x2+1, y1:y2+1] ^= True
    elif op == 'turn on':
      G[x1:x2+1, y1:y2+1] = 1
    elif op == 'turn off':
      G[x1:x2+1, y1:y2+1] = 0
  return G.sum()

def two(INPUT):
  G = numpy.zeros((1000, 1000), dtype=numpy.int32)
  instrs = parse(INPUT)
  for (op, x1, y1, x2, y2) in instrs:
    if op == 'toggle': 
      G[x1:x2+1, y1:y2+1] += 2
    elif op == 'turn on':
      G[x1:x2+1, y1:y2+1] += 1
    elif op == 'turn off':
      G[x1:x2+1, y1:y2+1] -= 1
      G = numpy.maximum(G, 0)

  return G.sum()

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "6")

  p.run(one, 0)
  p.run(two, 0)

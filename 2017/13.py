#!/usr/bin/env python3
import puzzle, library
import re

def parse(INPUT):
  pat = re.compile('(\d+): (\d+)')
  for l in INPUT:
    yield list(map(int, re.match(pat, l).groups()))

def run(layers, offset=0):
  caught_layers = []
  for layer, depth in layers:
    if (layer+offset) % (2*(depth-1)) == 0:
      caught_layers.append(layer)
  return caught_layers

def one(INPUT):
  layers = list(parse(INPUT))
  caught_layers = run(layers)
  total = 0

  for layer, depth in layers:
    if layer in caught_layers:
      total += layer*depth
  return total

def two(INPUT):
  layers = list(parse(INPUT))
  for i in range(5000000):
    if len(run(layers, offset=i)) == 0:
      return i

p = puzzle.Puzzle("2017", "13")
p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle, re, library

def parse_input(INPUT):
  return INPUT

def iter(G):
  new_G = library.Grid(x=G.max_x(), y= G.max_y())
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      neighbors = list(G.neighbors((x, y))).count('#')
      if G.get((x, y)) == '#' and neighbors != 1:
        new_G.set((x, y), '.')
      elif G.get((x, y)) == '.' and neighbors in [1, 2]:
        new_G.set((x, y), '#')
      else:
        new_G.set((x, y), G.get((x, y)))
  return new_G

def score(G):
  val = 0
  mag = 1
  for y in range(G.max_y()):
    for x in range(G.max_x()):
      if G.get((x, y)) == '#':
        val += mag
      mag *= 2
  return val

def one(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  seen = set()
  while True:
    key = str(G)
    if key in seen:
      return score(G)
    seen.add(key)
    G = iter(G)

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

p = puzzle.Puzzle("2019", "24")
p.run(one, 0)
p.run(two, 0)

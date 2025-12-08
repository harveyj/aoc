#!/usr/bin/env python3
import puzzle, library
from functools import lru_cache

def one(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  start = G.detect("S")[0]
  beams = [start]
  out = 0
  while beams:
    beam = beams.pop()
    G.set(beam, "|")
    new_loc = beam[0], beam[1] + 1
    if G.get(new_loc, default="#") == ".":
      beams.append(new_loc)
    elif G.get(new_loc, default="#") == "^":
      out += 1
      l = new_loc[0]-1, new_loc[1]
      r = new_loc[0]+1, new_loc[1]
      if not l in beams: beams.append(l)
      if not r in beams: beams.append(r)
    elif G.get(new_loc, default="#") == "#": pass
  return out

def two(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  start = G.detect("S")[0]
  @lru_cache(maxsize=None)
  def worlds(G, loc):
    new_loc = loc[0], loc[1] + 1
    if G.get(new_loc, default="#") == ".":
      return worlds(G, new_loc)
    elif G.get(new_loc, default="#") == "^":
      l = new_loc[0]-1, new_loc[1]
      r = new_loc[0]+1, new_loc[1]
      return worlds(G, l) + worlds(G, r)
    elif G.get(new_loc, default="#") == "#": return 1

  return worlds(G, start)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "7")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

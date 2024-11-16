#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx

def parse(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

def one(INPUT, two=False):
  def iter(G):
    G2 = library.Grid(x=G.max_x(), y=G.max_y())
    for x in range(G.max_x()):
      for y in range(G.max_y()):
        neigh = [item for item in G.neighbors_diag((x, y)) if item == '#']
        # print(len(neigh))
        if len(neigh) == 3 or G.get((x, y)) == "#" and len(neigh) == 2:
          G2.set((x, y), '#')
    return G2
  G = parse(INPUT)
  if two:
    print('override')
    G.set((0,0), '#'); G.set((0,G.max_y()-1), '#'); G.set((G.max_x()-1,0), '#'); G.set((G.max_x()-1,G.max_y()-1), '#'); 

  for i in range(100):
    G = iter(G)
    print(G)
    print("")
    if two:
      print('override')
      G.set((0,0), '#'); G.set((0,G.max_y()-1), '#'); G.set((G.max_x()-1,0), '#'); G.set((G.max_x()-1,G.max_y()-1), '#'); 

  tot = 0
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == '#': tot += 1
  return tot

def two(INPUT):
  return one(INPUT, two=True)

p = puzzle.Puzzle("2015", "18")
p.run(one, 0)
p.run(two, 0)

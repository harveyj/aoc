#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
from collections import defaultdict

def one(INPUT):
  class Grid(object):
    def __init__(self, INPUT):
      self.grid = library.Grid(raw='\n'.join(INPUT))
      self.portals = defaultdict(list)
      self.overlay_pts = []
      self.scrub()

    def scrub(self):
      for x in range(self.grid.max_x()):
        for y in range(self.grid.max_y()):
          triplet = ''.join((self.grid.get((x, y), ' '), self.grid.get((x+1, y), ' '), self.grid.get((x+2, y), ' ')))
          loc = None
          if re.match(r'\.[A-Z][A-Z]', triplet):
            key = triplet[1:]
            loc = (x, y)
          if re.match(r'[A-Z][A-Z]\.', triplet):
            key = triplet[:-1]
            loc = (x+2, y)
          if loc:
            self.portals[key] += (loc,)
            self.grid.set(loc, '@')
          loc = None
          triplet = "".join((self.grid.get((x, y), ' '), self.grid.get((x, y+1), ' '), self.grid.get((x, y+2), ' ')))
          if re.match(r'\.[A-Z][A-Z]', triplet):
            key = triplet[1:]
            loc = (x, y)
          if re.match(r'[A-Z][A-Z]\.', triplet):
            key = triplet[:-1]
            loc = (x, y+2)
          if loc: 
            self.portals[key] += (loc,)
            self.grid.set(loc, '@')


  grid = Grid(INPUT)
  G = grid.grid
  graph = nx.Graph()
  sloc = grid.portals['AA'][0]
  eloc = grid.portals['ZZ'][0]
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      val = G.get((x, y))
      for neigh_loc, neigh_val in G.neighbors_kv((x, y), default=' '):
        if val not in '# ' and neigh_val not in '# ':
          graph.add_edge((x, y), neigh_loc)
  for key in grid.portals:
    if len(grid.portals[key]) == 2:
      a, b = grid.portals[key] 
      graph.add_edge(a, b)

  return nx.shortest_path_length(graph, sloc, eloc)

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "20")

  print(p.run(one, 0))
  # p.run(two, 0)

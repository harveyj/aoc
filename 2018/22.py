#!/usr/bin/env python3
import puzzle, re, library
import networkx as nx

def one(INPUT, two=False):
  erosionG = library.Grid(x=100, y=1000)
  terrainG = library.Grid(x=100, y=1000)
  depth = library.ints(INPUT[0])[0]
  tgt = tuple(library.ints(INPUT[1]))
  TERRAIN_TYPES='.=|'
  for x in range(erosionG.max_x()):
    for y in range(erosionG.max_y()):
      if x == 0: erosionG.set((x, y), (y*48271+depth) % 20183)
      elif y == 0: erosionG.set((x, y), (x*16807+depth) % 20183)
      else: erosionG.set((x, y), (erosionG.get((x-1, y)) * erosionG.get((x, y-1)) + depth) % 20183)
      if (x, y) == tgt: erosionG.set((x, y), depth%20183)
      terrainG.set((x, y), TERRAIN_TYPES[erosionG.get((x, y)) % 3])
  tot = 0
  for x in range(tgt[0]+1):
    for y in range(tgt[1]+1):
      tot += TERRAIN_TYPES.index(terrainG.get((x, y)))
  if two: return terrainG
  return tot

TOOLS = "CTN"
LEGAL_TOOLS={'.': 'CT', '=': 'CN', '|': 'TN'}

def two(INPUT):
  terrainG = one(INPUT, two)
  graph = nx.Graph()
  tgt = tuple(library.ints(INPUT[1]))
  for x in range(terrainG.max_x()):
    for y in range(terrainG.max_y()):
      loc = (x, y)
      terrain = terrainG.get(loc)
      graph.add_edge((loc, LEGAL_TOOLS[terrain][0]), (loc, LEGAL_TOOLS[terrain][1]), weight=7)
      for neigh_loc, neigh_terrain in terrainG.neighbors_kv(loc):
        if not neigh_terrain: continue
        valid_tools = set(LEGAL_TOOLS[terrain]).intersection(set(LEGAL_TOOLS[neigh_terrain]))
        for vt in valid_tools:
          graph.add_edge((loc, vt), (neigh_loc, vt), weight=1)
  sp = nx.shortest_path_length(graph, source=((0,0), 'T'), target=(tgt, 'T'), weight='weight')
  return sp

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "20")
  print(p.run(one, 0))
  print(p.run(two, 0))
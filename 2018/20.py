#!/usr/bin/env python3
import puzzle, library
import networkx as nx

N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0) 
DIRS=dict(zip('NSEW', [N, S, E, W]))

def parse(buf, start, G, loc):
  idx = start
  if start == len(buf) or buf[idx] == ')': return 0
  while idx < len(buf) and buf[idx] not in '(|)': 
    G.set(loc, '.')
    dir = DIRS[buf[idx]]
    loc = library.pt_add(loc, dir)
    G.set(loc, '-' if buf[idx] in 'NS' else '|')
    loc = library.pt_add(loc, dir)
    G.set(loc, '.')
    idx += 1
  if idx == len(buf) or buf[idx] in '|)': return idx-start
  # we encountered (, so recurse in
  while idx < len(buf) and buf[idx] != ')':
    # skip the leading chars ( | - of the or block
    idx += 1
    consumed = parse(buf, idx, G, loc)
    idx += consumed
    # print(buf[idx:])
  idx += parse(buf, idx + 1, G, loc)
  return idx - start + 1 # +1 to consume closing )

def one(INPUT, two=False):
  SIZE = 1000
  G = library.Grid(x=SIZE, y=SIZE)
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      G.set((x, y), '#')
  start = SIZE//2, SIZE//2
  parse(INPUT[0][1:-1], 0, G, start)
  graph = G.graph(permissible='.|-')
  paths = nx.single_source_shortest_path(graph, start)
  paths = {k: paths[k] for k in paths if G.get(k) == '.'}
  if two: return paths
  return max(len(p) for p in paths.values()) // 2

def two(INPUT):
  paths = one(INPUT, two=True)
  return len([p for p in paths.values() if len(p)//2 >= 1000])

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "20")
  print(p.run(one, 0))
  print(p.run(two, 0))
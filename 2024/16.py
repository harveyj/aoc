#!/usr/bin/env python3
import puzzle, library
import networkx as nx

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  S = G.detect('S')[0]
  E = G.detect('E')[0]
  return G, S, E

DIRS = library.DIRS_CARDINAL

def one(INPUT, two=False):
  G, S, E = parse_input(INPUT)
  graph = nx.DiGraph()
  start_idx = 0 # start facing east
  dir_idx = start_idx
  queue = [(S, dir_idx)]
  seen = set()
  for n in range(4): graph.add_edge((E, n), E, weight=0)
  while queue:
    loc, dir_idx = queue.pop()
    if (loc, dir_idx) in seen: continue
    # invariant: we are at a junction. you may be able to go straight, you may be able to turn
    # go straight
    new_loc = library.pt_add(loc, DIRS[dir_idx])
    if G.get(new_loc) in 'SE.':
      graph.add_edge((loc, dir_idx), (new_loc, dir_idx), weight=1)
      queue.append((new_loc, dir_idx))
    # can you turn left/right (iow, is left/right then straight legal)
    for new_dir_idx in [(dir_idx + 3) % 4, (dir_idx + 1) % 4]:
      if loc == S: print('start new dir idx', dir_idx, new_dir_idx)
      graph.add_edge((loc, dir_idx), (loc, new_dir_idx), weight=1000)
      queue.append((loc, new_dir_idx))
    seen.add((loc, dir_idx))

  paths = nx.all_shortest_paths(graph, source=(S, start_idx), target=E, weight='weight')
  in_shortest = set()
  for p in paths:
    for loc, dir in p:
      in_shortest.add(loc)
  if two: return len(in_shortest) - 1 # TODO code smell
  return nx.dijkstra_path_length(graph, (S, start_idx), E)

two = lambda INPUT: one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "16")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
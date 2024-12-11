#!/usr/bin/env python3
import puzzle, re, networkx, collections, library

def parse_input(INPUT):
  G = networkx.DiGraph()
  grid = library.Grid(raw='\n'.join(INPUT))
  for x in range(grid.max_x()):
   for y in range(grid.max_y()):
      pt = (x,y)
      if two:
        if grid.get(pt) in '.><^v':
          G.add_node(pt)
          for neighbor in grid.neighbors_locs(pt):
            if grid.get(neighbor, default='#') in '.><v^':
              G.add_edge(pt, neighbor)
        continue
      if grid.get(pt) == '.':
        G.add_node(pt)
        for neighbor in grid.neighbors_locs(pt):
          if grid.get(neighbor, default='#') in '.><v^':
            G.add_edge(pt, neighbor)
      elif grid.get(pt) == '>':
        G.add_node(pt)
        r = (pt[0]+1, pt[1])
        if (grid.get(r, default='#') in '.v^<>'):
          G.add_edge(pt, r)
      elif grid.get(pt) == 'v':
        G.add_node(pt)
        d = (pt[0], pt[1]+1)
        if (grid.get(d, default='#') in '.<>v^'):
          G.add_edge(pt, d)
  S = 1, 0
  E = grid.max_x() - 2, grid.max_y()-1
  grid.overlays[S] = 'S'
  grid.overlays[E] = 'E'
  return S, E, G, grid

def parse_input_2(INPUT):
  G = networkx.Graph()
  grid = library.Grid(raw=INPUT)
  for x in range(grid.max_x()):
   for y in range(grid.max_y()):
      pt = (x,y)
      if grid.get(pt) in '.><^v':
        G.add_node(pt)
        grid.set(pt, '.')
        for neighbor in grid.neighbors_locs(pt):
          if grid.get(neighbor, default='#') in '.><v^':
            G.add_edge(pt, neighbor)
      S = 1, 0
  E = grid.max_x() - 2, grid.max_y()-1
  grid.overlays[S] = 'S'
  grid.overlays[E] = 'E'
  return S, E, G, grid

def one(INPUT):
  S, E, G, grid = parse_input(INPUT)
  all_paths = list(networkx.all_simple_paths(G, S, E))
  out_path = max(all_paths, key=lambda x: len(x))
  # print(len(all_paths))
  for path in all_paths:
    # print(path)
    for pt in path:
      # print(pt)
      if grid.get(pt) == '.': 
        grid.overlays[pt] = 'O'
  # print(grid)
  return len(out_path) - 1

def bfs_corners(grid, G, S, corners):
  accessible_corners = []
  for start in grid.neighbors_locs(S):
    if grid.get(start) != '.': continue
    queue = collections.deque([start])
    seen = set([S])
    length = 0
    while queue:
      length += 1
      node = queue.pop()
      if node in corners:
        accessible_corners.append((node, length))
      else:
        seen.add(node)
        for _, dst in G.edges(node):
          if dst not in seen:
            queue.append(dst)
  return accessible_corners

def two(INPUT):
  S, E, G, grid = parse_input_2(INPUT)
  # all_paths = networkx.all_simple_paths(G, S, E)
  # out_path = max(all_paths, key=lambda x: len(x))
  G2 = networkx.Graph()
  # print(G.nodes)
  corners = set([S, E])
  for x in range(grid.max_x()):
    for y in range(grid.max_y()):
      pt = x, y
      if grid.get(pt) == '.' and list(grid.neighbors(pt)).count('.') > 2:
        corners.add(pt)
        grid.overlays[pt] = 'C'
  for c in corners:
    G2.add_node(c)
    for c2, length in bfs_corners(grid, G, c, corners):
      print(c, c2, length)
      G2.add_edge(c, c2, weight=length)
  all_paths = [(path, networkx.path_weight(G2, path, weight='weight'))
               for path in networkx.all_simple_paths(G2, S, E)]
  out_path = max(all_paths, key=lambda x: x[1])
  print(out_path)
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "23")

  p.run(one, 0) 
  p.run(two, 0) 

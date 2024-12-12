#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict, deque

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  return G

def find_region(G, G_labeled, seen, start):
  region = set(); region.add(start)
  queue = deque([start])
  val = G.get(start)
  G_labeled.set(start, start)
  while queue:
    item = queue.pop()
    seen.add(item)
    for new_loc, new_val in G.neighbors_kv(item):
      if new_val == val and new_loc not in seen:
        queue.append(new_loc)
        region.add(new_loc)
        G_labeled.set(new_loc, start)
  return region

def one(INPUT):
  G = parse_input(INPUT)
  G_labeled = library.Grid(x=G.max_x(), y=G.max_y())
  seen = set()
  regions = dict() # key = loc, val = set of locs
  borders = defaultdict(int)
  edges = defaultdict(int)

  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if (x, y) in seen: continue
      region = find_region(G, G_labeled, seen, (x, y))
      regions[(x, y)] = region
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      border_same = len([n for n in G.neighbors((x, y)) if n == G.get((x, y))])
      borders[G_labeled.get((x, y))] += 4 - border_same

  return sum([len(regions[r]) * borders[r] for r in regions])

def two(INPUT):
  G = parse_input(INPUT)
  G_labeled = library.Grid(x=G.max_x(), y=G.max_y())
  seen = set()
  regions = dict() # key = loc, val = set of locs
  edges = defaultdict(list)

  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if (x, y) in seen: continue
      region = find_region(G, G_labeled, seen, (x, y))
      regions[(x, y)] = region

  passes_lr = (('l', [-1, 0]),  ('r', [1, 0]))
  passes_ud = (('u', [0, -1]), ('d', [0, 1]))

  for type, delta in passes_lr:
    for x in range(G.max_x()):
      y = 0
      while y < G.max_y():
        pt = (x, y)
        d_pt = library.pt_add(pt, delta)
        val = G.get(pt)
        dval = G.get(d_pt)
        y += 1
        if dval != val:
          edges[pt] += type
          while G.get((x, y)) == val and G.get(library.pt_add((x, y), delta)) != val:
            y += 1

  for type, delta in passes_ud:
    for y in range(G.max_y()):
      x = 0
      while x < G.max_x():
        pt = (x, y)
        d_pt = library.pt_add(pt, delta)
        val = G.get(pt)
        dval = G.get(d_pt)
        x += 1
        if G.get(d_pt) != val:
          edges[pt] += type
          while G.get((x, y)) == val and G.get(library.pt_add((x, y), delta)) != val:
            x += 1
  costs = []
  for r in regions:
    costs.append(((G.get(list(regions[r])[0]), len(regions[r]), sum([len(edges[loc]) for loc in regions[r]]))))
  return sum([a[1] * a[2] for a in costs])

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "12")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

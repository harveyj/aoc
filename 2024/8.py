#!/usr/bin/env python3
import puzzle, library, itertools
from collections import defaultdict

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  locs = defaultdict(list)
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      c = G.get((x, y))
      if c != '.':
        locs[c].append((x,y))
  nodes = defaultdict(list)
  seen = set()
  for c in locs:
    for p0, p1 in itertools.combinations(locs[c], 2):
      dx = p0[0] - p1[0]; dy = p0[1] - p1[1]
      n1 = (p0[0] - 2 * dx, p0[1] - 2 * dy)
      n2 = (p0[0] + dx, p0[1] + dy)
      if G.legal(n1): 
        nodes[n1].append(c)
        seen.add(n1)
      if G.legal(n2):
        nodes[n2].append(c)
        seen.add(n2)
  nodes = {key: '#' for key in nodes.keys()}
  G.overlays = nodes
  print(G)
  return len(seen)

def is_int(num, tolerance = 1e-3):
  return abs(round(num) - num) < tolerance

# The initial and IMO cleanest
def two(INPUT):
  locs = defaultdict(list)
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      c = G.get((x, y))
      if c != '.':
        locs[c].append((x,y))
  # print(locs)
  nodes = defaultdict(list)
  seen = set()
  for c in locs:
    for p0, p1 in itertools.combinations(locs[c], 2):
      dx = p0[0] - p1[0]
      dy = p0[1] - p1[1]
      if dy == 0:
        sx = 1.0; sy = 0
      else: 
        sx = dx/dy; sy = 1.0
      pt = p0
      while G.legal(pt):
        nodes[pt].append(c)
        seen.add(pt)
        pt = library.pt_add(pt, (sx, sy))
        if is_int(pt[0]) and is_int(pt[1]):
          pt = round(pt[0]), round(pt[1])
      pt = p0
      while G.legal(pt):
        nodes[pt].append(c)
        seen.add(pt)
        pt = library.pt_add(pt, (-sx, -sy))
        if is_int(pt[0]) and is_int(pt[1]):
          pt = round(pt[0]), round(pt[1])
 
  seen = set([(round(pt[0]), round(pt[1])) for pt in seen if is_int(pt[0]) and is_int(pt[1])])
  print(seen)
  overlays = {item: '#' for item in seen}
  G.overlays = overlays
  print(G)
  return len(seen)

# This was the first one and even bruter-force.
def two_alt(INPUT):
  locs = defaultdict(list)
  G = library.Grid(raw='\n'.join(INPUT))
  
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      c = G.get((x, y))
      if c != '.':
        locs[c].append((x,y))

  anti = set()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      for c in locs:
        for p0, p1 in itertools.combinations(locs[c], 2):
          if (x, y) in [p0, p1]:
            anti.add((x, y))
            continue
          if x - p0[0] == 0:
            continue
          else: 
            slope1 = (y - p0[1]) / (x - p0[0])
          if x - p1[0] == 0:
            continue
          else:
            slope2 = (y - p1[1]) / (x - p1[0])
          if slope1 == slope2:
            anti.add((x, y))
  overlays = {item: '#' for item in anti}
  G.overlays = overlays
  print(G)
  return len(anti)

p = puzzle.Puzzle("2024", "8")
# p.run(one, 0)
p.run(two_old, 0)
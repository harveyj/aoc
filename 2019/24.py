#!/usr/bin/env python3
import puzzle, re, library
from itertools import chain

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

def neighbors(grids, layer, pt):
  x, y = pt
  u, d, l, r = ([grids[layer].get((x + dx, y + dy))] for (dx, dy) in ((0, -1), (0, 1), (-1, 0), (1, 0)))

  if y == 0:
    u = [grids[layer + 1].get((2, 1))]
  if y == 4:
    d = [grids[layer + 1].get((2, 3))]
  if x == 0:
    l = [grids[layer + 1].get((1, 2))]
  if x == 4:
    r = [grids[layer + 1].get((3, 2))]
  
  if (x, y) == (1, 2):
    r = [grids[layer - 1].get((0, y)) for y in range(5)]
  elif (x, y) == (2, 1):
    d = [grids[layer - 1].get((x, 0)) for x in range(5)]
  elif (x, y) == (2, 3):
    u = [grids[layer - 1].get((x, 4)) for x in range(5)]
  elif (x, y) == (3, 2):
    l = [grids[layer - 1].get((4, y)) for y in range(5)]
  
  return list(chain.from_iterable([u, d, l, r]))
  


def two(INPUT):
  depth = 300
  g_0 = library.Grid(raw='\n'.join(INPUT))
  grids = [library.Grid(x=5, y=5) for i in range(depth)] + [g_0] + [library.Grid(x=5, y=5) for i in range(depth)]

  print(grids[depth])
  print('')

  for i in range(200):
    new_grids = [library.Grid(x=5, y=5) for i in range(depth*2+1)]
    for j in range(1, 2*depth):
      G = grids[j]
      new_G = new_grids[j]
      new_G.overlays[(2,2)] = '?'
      for x in range(G.max_x()):
        for y in range(G.max_y()):
          # if (x, y) == (2, 2) and j != 0: continue
          neighbor_raw = neighbors(grids, j, (x, y))
          neighbor_count = neighbor_raw.count('#')
          # if j == depth: print(f'x {x}, y {y}, nc {neighbor_count}')
          if G.get((x, y)) == '#' and neighbor_count != 1:
            new_G.set((x, y), '.')
          elif G.get((x, y)) == '.' and neighbor_count in [1, 2]:
            new_G.set((x, y), '#')
          else:
            new_G.set((x, y), G.get((x, y)))
    grids = new_grids

    # print(i+1)
    # for j in range(depth-5, depth+5):
    #   print(j)
    #   print(grids[j])
  for G in grids:
    G.set((2,2), '.')
  return sum([len(G.detect('#')) for G in grids])


def test():
  grids = [library.Grid(x=5, y=5) for i in range(10)]
  grids[5] = library.Grid(grid=['ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY']) 
  grids[6] = library.Grid(grid=['12345', '67890', [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21,22,23,24,25]])

  # print(neighbors(grids, 6, (3,3))) 
  # print(neighbors(grids, 5, (1,1))) 
  # print(neighbors(grids, 5, (3,0))) 
  # print(neighbors(grids, 5, (4,0))) 
  # print(neighbors(grids, 6, (3,2))) 
  # print(neighbors(grids, 5, (3,2))) 


  print(neighbors(grids, 6, (1,2))) 
  print(neighbors(grids, 6, (3,2))) 
  print(neighbors(grids, 6, (2, 3))) 
  print(neighbors(grids, 6, (2, 1))) 

  print(neighbors(grids, 5, (0,0))) 
  print(neighbors(grids, 5, (0,1))) 
  print(neighbors(grids, 5, (0,2))) 
  print(neighbors(grids, 5, (0,3))) 
  print(neighbors(grids, 5, (0,4))) 
  
  print(neighbors(grids, 5, (1,0))) 
  print(neighbors(grids, 5, (1,1))) 
  # print(neighbors(grids, 5, (1,2))) 
  print(neighbors(grids, 5, (1,3))) 
  print(neighbors(grids, 5, (1,4))) 

  print(neighbors(grids, 5, (2,0))) 
  # print(neighbors(grids, 5, (2,1)))
  # print(neighbors(grids, 5, (2,2))) 
  # print(neighbors(grids, 5, (2,3))) 
  print(neighbors(grids, 5, (2,4))) 



p = puzzle.Puzzle("2019", "24")
# p.run(one, 0)
p.run(two, 0)
# test()
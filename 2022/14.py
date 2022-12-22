#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT, bottom=False):
  BUFFER = 200
  min_x = 1000000
  min_y = 1000000

  max_x = 0
  max_y = 0 
  pts = []
  for l in INPUT.split('\n'):
    sx, sy = None, None
    for pt in re.finditer("(\d+),(\d+)", l):
      x, y = map(int, pt.groups(1))
      max_x = max(max_x, x)
      max_y = max(max_y, y)
      min_x = min(min_x, x)
      min_y = min(min_y, y)
      if sx and sx != x:
        mag = abs(sx - x)
        for i in range(0, mag+1):
          pts.append(((sx - i * (sx-x) // mag), y))
      elif sy and sy != y:
        mag = abs(sy - y)
        for i in range(0, mag+1):
          pts.append((x, (sy - i * (sy-y) // mag)))
      sx = x
      sy = y
  pts = [(x, y) for x, y in pts]
  g = Grid(max_x + BUFFER, max_y + BUFFER)
  for pt in pts:
    g.set(pt, '#')
  if bottom:
    for x in range(min_x-BUFFER, max_x+BUFFER):
      g.set((x, max_y + 2), '#')
  return g, (500, 0), (max_x, max_y)

class Grid:
  def __init__(self, x, y):
    self.x = x; self.y = y
    self.grid = [["." for i in range(x)] for j in range(y)]

  def set(self, pt, val):
    x, y = pt
    self.grid[y][x] = val

  def get(self, pt):
    x, y = pt
    return self.grid[y][x]

  def __str__(self):
    return '\n'.join([''.join(row) for row in self.grid])

  def window(self, min_x, min_y, max_x, max_y):
    return '\n'.join([''.join(row[min_x:max_x]) for row in self.grid[min_y:max_y]])



def drop_one(grid, start, bottom_y):
  x, y = start
  if grid.get(start) == 'o':
    return False
  while True:
    if y == bottom_y+3:
      print('bail')
      return False
    if grid.get((x, y+1)) == '.':
      x, y = (x, y+1)
    elif grid.get((x-1, y+1)) == '.':
      x, y = (x-1, y+1)
    elif grid.get((x+1, y+1)) == '.':
      x, y = (x+1, y+1)
    else:
      grid.set((x, y), 'o')
      return True
    

def one(INPUT):
  grid, o_start, max_pt = parse(INPUT)
  max_y = max_pt[1]
  grid.set(o_start, '+')
  grains = 0
  while drop_one(grid, o_start, max_y):
    grains += 1

  print(grid)
  return grains

def two(INPUT):
  grid, o_start, max_pt = parse(INPUT, bottom=True)
  max_y = max_pt[1]
  grid.set(o_start, '+')
  grains = 0
  while drop_one(grid, o_start, max_y):
    grains += 1
  print(grid.window(490, 0, 510, 20))
  return grains

p = puzzle.Puzzle("14")
# p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict, namedtuple
import networkx as nx
import itertools
import statistics

Cell = namedtuple('Cell', ['x', 'y', 'dx', 'dy'])

def parse_input(INPUT):
  for l in INPUT:
    yield Cell(*library.ints(l))

def one(INPUT, two=False):
  cells = list(parse_input(INPUT))
  G = library.Grid(x=1500, y=1000)
  min_std_dev = 10000000
  min_i_val = 0
  for i in range(0, 20000):
    cells = [Cell(x+dx, y+dy, dx, dy) for (x, y, dx, dy) in cells]
    G.overlays = {(c.x, c.y): '$' for c in cells}
    stddev = statistics.stdev([c.x for c in cells])
    # This works if you start it at zero but this saves time.
    if i > 10700 and stddev < min_std_dev:
      min_x = max(cells[0][0] - 50, 0); min_y = max(cells[0][1] - 50, 0)
      print(G.window(min_x, min_y, min_x + 100, min_y + 100))
      min_std_dev = stddev
      min_i_val = i
  # Read the letters off of the grid
  return min_i_val if two else 'DUMMY'

def two(INPUT):
  return one(two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "10")
  print(p.run(one, 0))
  print(p.run(two, 0))
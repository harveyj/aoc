#!/usr/bin/env python3
import puzzle, networkx
from itertools import product

def parse_input(INPUT):
  return puzzle.Grid(raw=INPUT)

deltas = {'N': (0, -1), 
          'S': (0, 1), 
          'E': (1, 0), 
          'W': (-1, 0), 
          }

legal_turns = {'N': ['E', 'W'],
                'W': ['N', 'S'],
                'E': ['N', 'S'],
                'S': ['E', 'W'],
                '*': ['N', 'S', 'E', 'W']
                }

def mul_vect(vect, mag):
  return [i * mag for i in vect]

def find_longest_path(INPUT, min, max):
  def add_edges(G, pt, prev_dir):
    x, y = pt
    for new_dir in legal_turns[prev_dir]:
      for steps in range(min, max+1):
        dx, dy = deltas[new_dir]
        tgt = puzzle.pt_add((x, y), mul_vect((dx, dy), steps))
        weight = sum([int(grid.get((x + dx * i, y + dy * i), default=10000)) for i in range(1,steps+1)])
        if grid.get(tgt, default=None):

          G.add_edge(((x, y), prev_dir), (tgt, new_dir), weight=weight)

  grid = parse_input(INPUT)
  G = networkx.DiGraph()
  for x in range(grid.max_x()):
    for y in range(grid.max_y()):
      for prev_dir in ['N', 'S', 'E', 'W']:
        G.add_node(((x, y), prev_dir))
        add_edges(G, (x, y), prev_dir)
  G.add_node('START')
  add_edges(G, (0,0), '*')
  G.add_edge('START', ((0,0), '*'), weight=0)
  G.add_node('END')
  for prev_dir in ['N', 'S', 'E', 'W']:
    G.add_edge(((grid.max_x() -1, grid.max_y() -1), prev_dir), 'END', weight=0)

  return networkx.dijkstra_path_length(G, source='START', target='END')

def one(INPUT):
  return find_longest_path(INPUT, 1, 3)

def two(INPUT):
  return find_longest_path(INPUT, 4, 10)


if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "17")

  p.run(one, 0) 
  p.run(two, 0) 

#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

def shift(dir, G):
  dir_vars = {'up': (0, -1, 0, G.max_x(), 1, 0, G.max_y(), 1),
              'down': (0, 1, 0, G.max_x(), 1, G.max_y(), -1, -1),
              'left': (-1, 0, 0, G.max_x(), 1, 0, G.max_y(), 1),
              'right': (1, 0, G.max_x(), -1, -1, 0, G.max_y(), 1),
               }
  dx, dy, start, end, step, start2, end2, step2 = dir_vars[dir]
  for x in range(start, end, step):
    for y in range(start2, end2, step2):
      if G.get((x, y), '#') == 'O':
        pt_dest = library.pt_add((x, y), (dx, dy))
        while G.get(pt_dest, '#') == '.':
          pt_dest = library.pt_add(pt_dest, (dx, dy))
        pt_dest = library.pt_add(pt_dest, (-dx, -dy))
        if pt_dest != (x, y):
          G.set(pt_dest, 'O')
          G.set((x, y), '.')
  return None

def find_loop(G):
  cache = dict()
  for i in range(10000):
    # if i % 10 == 0: print('.', end='')
    for dir in ['up', 'left', 'down', 'right']:
      shift(dir, G)
    raw = G.__hash__()
    if raw in cache:
      return i, i - cache[raw]
    cache[raw] = i

def score(G):
  out = 0
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == 'O':
        out += G.max_y() - y
  return out

def one(INPUT):
  G = parse_input(INPUT)
  G = shift('up', G)
  return score(G)

def two(INPUT):
  G = parse_input(INPUT)
  start, period = find_loop(G)
  # print(start, period)
  cycles_left = (1000000000-start) % period - 1
  for i in range(cycles_left):
    for dir in ['up', 'left', 'down', 'right']:
      shift(dir, G)
    # print(score(G))
  return score(G)

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "14")

  p.run(one, 1) 
  p.run(two, 0) 
# cProfile.run('p.run(two, 0)')

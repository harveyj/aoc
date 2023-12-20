#!/usr/bin/env python3
import puzzle, re, math
from puzzle import pt_add

def parse_input(INPUT):
  G = puzzle.Grid(grid=[list(l.strip()) for l in INPUT.strip().split('\n')])
  return G

def find_start(G):
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == 'S':
        return (x, y)

def seen(G):
  S = find_start(G)
  loc = S
  seen = set()
  start_code = ''
  dirs = {'-': ((-1, 0), (1, 0)), '|': ((0, 1), (0, -1)), 'F': ((1, 0), (0, 1)), 'J': ((-1, 0), (0, -1)),'7': ((-1, 0), (0, 1)),'L': ((1, 0), (0, -1)),}
  while len(seen) == 0 or loc != S:
    code = G.get(loc)
    # print(loc, code, len(seen))
    if code == 'S':
      seen.add(loc)
      legal_left, legal_up, legal_right, legal_down = False, False, False, False
      if G.get(pt_add(loc, (-1, 0))) in ['F', 'L', '-']: 
        legal_left = True
      if G.get(pt_add(loc, (1, 0))) in ['7', 'J', '-']:
        legal_right = True
      if G.get(pt_add(loc, (0, -1))) in ['F', '7', '|']: 
        legal_up = True
      if G.get(pt_add(loc, (0, 1))) in ['J', 'L', '|']:
        legal_down = True
      if legal_left and legal_up: start_code = 'J'
      if legal_left and legal_right: start_code = '-'
      if legal_left and legal_down: start_code = '7'
      if legal_up and legal_down: start_code = '|'
      if legal_right and legal_up: start_code = 'L'
      if legal_right and legal_down: start_code = 'F'
      code = start_code
    dir = dirs[code]
    for d in dir:
      if pt_add(loc, d) == S and len(seen) > 3: # ugh
         return seen, start_code
    x, y = pt_add(loc, dir[0])
    if (x, y) in seen:
      x, y = pt_add(loc, dir[1])
    if (x, y) in seen:
      print('ERROR', x, y, )
    loc = (x, y)
    seen.add(loc)

def one(INPUT):
  G = parse_input(INPUT)
  S, start_code = seen(G)
  return math.ceil(len(S) / 2)

def two(INPUT):
  G = parse_input(INPUT)
  L, start_code = seen(G)
  enclosed = set()
  toggles = set()
  for y in range(G.max_y()):
    in_loop = False
    x = -1
    while x < G.max_x():
      num_up, num_down = 0, 0
      x += 1
      if (x, y) in L:
        while x < G.max_x():
          code = G.get((x, y))
          if code == 'S': code = start_code
          if code in ['|', 'L', 'J']: num_up += 1
          if code in ['|', 'F', '7']: num_down += 1
          if num_up + num_down == 2:
            if num_up == num_down == 1:
              in_loop = not in_loop
              toggles.add((x, y))
            break
          x += 1

      elif in_loop:
        enclosed.add((x, y))
  for pt in enclosed: G.overlays[pt] = 'T'
  print(G)
  return len(enclosed)

# scan left
# if # edges %2 = 1, add this cell to enclosed
# if encountered path, consume all the rest in this path segment (until 2 exits)
#   if exit down + exit up, edges += 1
#   else edges += 2

p = puzzle.Puzzle("10")
# p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  for l in INPUT:
    yield (l[0], *library.ints(l))

E,S,W,N = library.DIRS_CARDINAL

stale = set()
overlays = dict()

def descend(G, src):
  if src in stale:
    overlays[src] = '@'
    return
  loc = src
  tot = G.detect_fast('|') + G.detect_fast('~')
  # go down from SRC until you hit water or clay
  while G.get(loc) in ['.', '|']:
    if G.get(loc) == '.': G.set(loc, '|')
    if G.get(library.pt_add(loc, W)) == '#' and G.get(library.pt_add(loc, E)) == '#':
      G.set(loc, '~')
    loc = library.pt_add(loc, S)
  if G.get(loc) == None:
    return
  # Back out the last move, which caused you to hit water/clay
  new_src = library.pt_add(loc, N)
  # go laterally in both directions
  # if you hit clay, terminate
  # if you hit air (pt below you is vacant) call descend on that point
  loc = new_src
  horiz_pts = set(); horiz_bounded = True
  while G.get(loc, '#') in '.|':
    horiz_pts.add(loc)
    loc = library.pt_add(loc, W)
    if G.get(library.pt_add(loc, S)) in '.|':
      horiz_pts.add(loc)
      descend(G, library.pt_add(loc, S))
      horiz_bounded = False
      break
  loc = library.pt_add(new_src, E)
  while G.get(loc, '#') in '.|':
    if G.get(library.pt_add(loc, S)) in '.|':
      horiz_pts.add(loc)
      descend(G, library.pt_add(loc, S))
      horiz_bounded = False
      break
    horiz_pts.add(loc)
    loc = library.pt_add(loc, E)
  for hp in horiz_pts: G.set(hp, '~' if horiz_bounded else '|')
  new_tot = G.detect_fast('|') + G.detect_fast('~')
  if new_tot == tot:
    stale.add(src)

def one(INPUT, two=False):
  lines = list(parse_input(INPUT))
  x_lines = [line for line in lines if line[0] == 'x']
  y_lines = [line for line in lines if line[0] == 'y']
  max_x = max([line[1] for line in x_lines])
  max_x = max(max_x, max([line[3] for line in y_lines]))
  min_y = min([line[2] for line in x_lines])
  max_y = max([line[1] for line in y_lines])
  max_y = max(max_y, max([line[3] for line in x_lines]))
  G = library.Grid(max_x+2, max_y+1)
  for _, y, s_x, e_x in y_lines:
    for x in range(s_x, e_x+1):
      G.set((x, y), '#')
  for _, x, s_y, e_y in x_lines:
    for y in range(s_y, e_y+1):
      G.set((x, y), '#')

  START = 500, min_y-1
  tot = 0; prev_tot = -1
  while True:
    descend(G, START)
    tot = G.detect_fast('|') + G.detect_fast('~')
    if tot == prev_tot:
      G.overlays = overlays
      if two: return G.detect_fast('~')
      return tot-1 # omit start
    prev_tot = tot

def two(INPUT):
  global stale
  stale = set()
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "17")
  print(p.run(one, 0))
  print(p.run(two, 0))

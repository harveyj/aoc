#!/usr/bin/env python3

import puzzle, library

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      G.set((x, y), int(G.get((x, y))))
  return G

def iter(G):
  new_G = library.Grid(x=G.max_x(), y=G.max_y())
  flashes = set()

  for x in range(G.max_x()):
    for y in range(G.max_y()):
      new_G.set((x, y), G.get((x, y)) + 1)

  new_flashes = ['dummy']
  while new_flashes != []:
    new_flashes = [fl for fl in new_G.detect(10) if fl not in flashes]
    for fl in new_flashes:
      flashes.add(fl)
      for x, y in G.neighbors_diag_locs(fl):
        if G.legal((x, y)): new_G.set((x, y), min(10, new_G.get((x, y)) + 1))
  for fl in flashes: new_G.set(fl, 0)
  return new_G, len(flashes)

def one(INPUT):
  G = parse_input(INPUT)
  flashes = []
  for i in range(100):
    G, n_flash = iter(G)
    flashes.append(n_flash)
  return sum(flashes)

def two(INPUT):
  G = parse_input(INPUT)
  for i in range(1000):
    G, _ = iter(G)
    if len(G.detect(0)) == G.max_x() * G.max_y():
      return i+1


if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "11")

  print(p.run(one, 0))
  print(p.run(two, 0))

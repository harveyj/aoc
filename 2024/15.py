#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict

def parse_input(INPUT):
  grid, moves = '\n'.join(INPUT).split('\n\n')
  moves = moves.replace('\n', '')
  G=library.Grid(raw=grid)
  return G, moves


def one(INPUT):
  G, moves = parse_input(INPUT)
  x, y = G.detect('@')[0]
  MOVE_DIR = dict(zip('><^v', [(1, 0), (-1, 0), (0, -1), (0, 1)])) 
  for m in moves.strip():
    dir = MOVE_DIR[m]
    nx, ny = x+dir[0], y+dir[1]
    while G.get((nx, ny)) == 'O':
      nx, ny = nx + dir[0], ny + dir[1]
    if G.get((nx, ny)) == '.':
      G.set((x, y), '.')
      G.set((nx, ny), 'O')
      x += dir[0]; y+= dir[1]
    G.overlays={(x, y): '@'}
    G.set((x, y), '.') # TODO code smell
  sum_gps = sum([loc[1]*100 + loc[0] for loc in G.detect('O')])
  return sum_gps


def double(G):
  new_G = library.Grid(x=G.max_x() * 2, y=G.max_y())
  out_map = {'#': '##', '@': '@.', '.': '..', 'O': '[]'}
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      outs = out_map[G.get((x, y))]
      new_G.set((x*2, y), outs[0])
      new_G.set((x*2 + 1, y), outs[1])
  return new_G

def shift(G, m):
  all_moves = []
  MOVE_DIR = dict(zip('><^v', [(1, 0), (-1, 0), (0, -1), (0, 1)]))
  start = G.detect('@')[0]
  impacted = set((start,))
  while impacted:
    new_impacted = set()
    while impacted:
      src_loc = impacted.pop()
      tgt_loc = library.pt_add(src_loc, MOVE_DIR[m])
      tgt_val = G.get(tgt_loc)
      all_moves.append((src_loc, tgt_loc))
      if tgt_val == '#':
        return G
      elif tgt_val in '[]':
        new_impacted.add(tgt_loc)
        if m in '^v':
          dx = 1 if tgt_val == '[' else -1
          new_impacted.add((tgt_loc[0] + dx, tgt_loc[1]))
      elif tgt_val == '@':
        new_impacted.add(tgt_loc)
    impacted = new_impacted
  for src, tgt in all_moves[::-1]:
    G.set(tgt, G.get(src))
    G.set(src, '.')
  G.set(start, '.')
  return G

def two(INPUT):
  G, moves = parse_input(INPUT); G = double(G)
  for m in moves.strip():
    G = shift(G, m)
  sum_gps = sum([loc[1]*100 + loc[0] for loc in G.detect('[')])
  return sum_gps

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "15")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
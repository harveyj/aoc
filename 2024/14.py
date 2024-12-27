#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict

def parse_input(INPUT):
  return [library.ints(l) for l in INPUT]

def iter(state, max_x, max_y):
  for robot in state:
    robot[0] = (robot[0] + robot[2]) + max_x 
    robot[1] = (robot[1] + robot[3]) + max_y
    robot[0] %= (max_x)
    robot[1] %= (max_y)

def make_grid(robots, MAX_X, MAX_Y):
  G = library.Grid(x=MAX_X, y=MAX_Y)
  for r in robots:
    r = r[0], r[1]
    if G.get(r) == '.':
      G.set(r, 1)
    else:
      G.set(r, G.get(r) + 1)
  return G

def one(INPUT):
  robots = parse_input(INPUT)
  MAX_X, MAX_Y = (101, 103)
  for i in range(100):
    iter(robots, MAX_X, MAX_Y)
  quads = defaultdict(list)
  for r in robots:
    w = r[0] < MAX_X / 2
    n = r[1] < MAX_Y / 2
    legal = r[0] != MAX_X //2 and r[1] != MAX_Y // 2
    if legal: quads[(w, n)].append(r)
  return len(quads[True, True]) * len(quads[True, False]) * len(quads[False, True]) * len(quads[False, False]) 

def two(INPUT):
  robots = parse_input(INPUT)
  MAX_X, MAX_Y = (101, 103)
  for i in range(0, 10404, 1):
    iter(robots, MAX_X, MAX_Y)
    G = make_grid(robots, MAX_X, MAX_Y)
    if '111111111111111' in str(G):
      return i + 1 # todo why

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "14")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

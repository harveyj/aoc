#!/usr/bin/env python3
import puzzle
import math

def parse(INPUT):
  return INPUT[0].split(',')

def one_1(INPUT):
  INPUT = parse(INPUT)
  n = INPUT.count('n') + 0.5 * (INPUT.count('nw') + INPUT.count('ne'))
  s = INPUT.count('s') + 0.5 * (INPUT.count('sw') + INPUT.count('se'))
  e = INPUT.count('e') + (INPUT.count('se') + INPUT.count('ne'))
  w = INPUT.count('w') + (INPUT.count('nw') + INPUT.count('sw'))
  print(n,s,e,w)
  ud = abs(n-s); lr = abs(e-w)
  return math.ceil(max(ud, lr))

def one_2(INPUT):
  INPUT = parse(INPUT)
  x=0; y=0
  cells = [(x, y)]
  for move in INPUT:
    if move == 'n':
      x += 0
      y += 1
    elif move == 's':
      x -= 0
      y -= 1
    elif move == 'ne':
      x += 1
      y += 0.5
    elif move == 'se':
      x += 1
      y -= 0.5
    elif move == 'nw':
      x -= 1
      y += 0.5
    elif move == 'sw':
      x -= 1
      y -= 0.5
    cells.append((x, y))
  print(cells)

  x, y = cells[-1]
  print(x,y)
  return math.ceil(max(abs(x), abs(y)))

# hint to look at hex grid coordinates
# https://www.redblobgames.com/grids/hexagons/
# 3-axis
def onetwo(INPUT):
  INPUT = parse(INPUT)
  q=0;s=0;r=0
  max_val = 0
  cells = [(q, s, r)]
  for move in INPUT:
    if move == 'n':
      q += 0
      s += 1
      r -= 1
    elif move == 's':
      q += 0
      s -= 1
      r += 1
    elif move == 'ne':
      q += 1
      s += 0
      r -= 1
    elif move == 'se':
      q += 1
      s -= 1
      r -= 0
    elif move == 'nw':
      q -= 1
      s += 1
      r -= 0
    elif move == 'sw':
      q -= 1
      s += 0
      r += 1
    cells.append((q, s, r))
    max_val = max(max_val, abs(q), abs(s), abs(r))
  # print(cells)

  q, s, r = cells[-1]
  return max(q, s, r), max_val


p = puzzle.Puzzle("2017", "11")
p.run(onetwo, 0)
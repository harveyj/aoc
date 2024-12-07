#!/usr/bin/env python3
import puzzle, re, networkx, math

def parse_input(INPUT):
  G = puzzle.Grid(raw=INPUT)
  pts = []
  for y in range(G.max_y()):
    for x in range(G.max_x()):
      if G.get((x, y)) == '#':
        pts.append((x, y))
  return G, pts

def check_blank(l):
  return len(l) == l.count('.')

def mod_distance(pt1, pt2, blank_rows, blank_cols, mul=1):
  pt1_x, pt1_y = pt1; pt2_x, pt2_y = pt2
  dx = abs(pt1_x - pt2_x)
  dy = abs(pt1_y - pt2_y)
  min_x = min(pt1_x, pt2_x); max_x = max(pt1_x, pt2_x)
  min_y = min(pt1_y, pt2_y); max_y = max(pt1_y, pt2_y)
  # print(min_x, max_x)
  skip_row = [y for y in blank_rows if min_y < y < max_y]
  skip_col = [x for x in blank_cols if min_x < x < max_x]
  # print('sc', skip_col)
  print(pt1, pt2, dx, dy, len(skip_row), len(skip_col), dx+dy+len(skip_row)*mul + len(skip_col)*mul)
  return dx+dy+len(skip_row)*mul + len(skip_col)*mul

def onetwo(INPUT):
  G, pts = parse_input(INPUT)
  blank_cols = [x for x in range(G.max_x()) if check_blank([G.get((x, y)) for y in range(G.max_y())])]
  blank_rows = [y for y in range(G.max_y()) if check_blank([G.get((x, y)) for x in range(G.max_x())])]
  
  out_1 = 0
  for i, pt1 in enumerate(pts):
    for j, pt2 in enumerate(pts[i+1:]):
      md = mod_distance(pt1, pt2, blank_rows, blank_cols)
      out_1 += md

  out_2 = 0
  for i, pt1 in enumerate(pts):
    for j, pt2 in enumerate(pts[i+1:]):
      md = mod_distance(pt1, pt2, blank_rows, blank_cols, mul=999999)
      out_2 += md

  return out_1, out_2

def one(INPUT):
  return onetwo(INPUT)[0]

def two(INPUT):
  return onetwo(INPUT)[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "11")

  p.run(one, 0) 
  p.run(two, 0) 

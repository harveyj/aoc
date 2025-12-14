#!/usr/bin/env python3
import puzzle, re, library
import numpy as np
def parse_input(INPUT):
  return [list(library.ints(l)) for l in INPUT]

def one(INPUT):
  invals = parse_input(INPUT)
  print(invals)
  vals = []
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
      vals.append(size(a, b))
  return max(vals)

def size(a, b):
  return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1]) +1)

def maxes(loc_a, loc_b):
  max_x = max(loc_a[0], loc_b[0])
  max_y = max(loc_a[1], loc_b[1])
  min_x = min(loc_a[0], loc_b[0])
  min_y = min(loc_a[1], loc_b[1])
  return (min_x, min_y, max_x, max_y)

# gives what side of the AB segment pt C > 0, < 0, == are left, right, collinear
def orient(a, b, c):
  # cross((b−a),(c−a))=(bx​−ax​)(cy​−ay​)−(by​−ay​)(cx​−ax​)
  return np.sign((b[0]-a[0]) * (c[1]-a[1]) - (b[1] - a[1]) * (c[0] - a[0]))

# Two line segments AB and CD intersect iff:
# C and D lie on opposite sides of line AB
# A and B lie on opposite sides of line CD
def intersect(a, b, c, d):
  o1 = orient(a, b, c)
  o2 = orient(a, b, d)
  o3 = orient(c, d, a)
  o4 = orient(c, d, b)
  return o1 != o2 and o3 != o4

def within(pt, vectors):
  # from 0, pt_y to pt
  lines = [vect for vect in vectors if intersect((0, pt[1]), pt, vect[0], vect[1])]
  active = False; last_active = -1
  for l in lines:
    if l[0][1] < l[1][1]:
      active = True
    else:
      last_active = l[0][0]
      active = False
  return active or pt[0] == last_active

def unimpeded(a, b, vectors):
  (min_x, min_y, max_x, max_y) = maxes(a, b)
  sides = [((min_x, min_y), (max_x, min_y)),  # top
            ((min_x, max_y), (max_x, max_y)), # bottom
            ((min_x, min_y), (min_x, max_y)), # left
            ((max_x, min_y), (max_x, max_y))  # right
          ]
  corners = within((min_x, min_y), vectors) and within((min_x, max_y), vectors) and within((max_x, max_y), vectors) and within((max_x, max_y), vectors)
  side = sides[0]
  top_lines = [vect for vect in vectors if intersect(side[0], side[1], vect[0], vect[1])]
  top_down_lines = [line for line in top_lines if line[0][1] < line[1][1] and line[1][1] > side[1][1]]

  side = sides[1]
  bottom_lines = [vect for vect in vectors if intersect(side[0], side[1], vect[0], vect[1])]
  bottom_up_lines = [line for line in bottom_lines if line[0][1] > line[1][1] and line[1][1] > side[1][1]]

  return corners and len(top_down_lines) == 0 and len(bottom_up_lines) == 0

def two(INPUT):
  invals = parse_input(INPUT)
  vectors = list(zip(invals, invals[1:] + [invals[0]]))
  vectors = sorted(vectors, key=lambda a: a[0][0])
  
  candidates = []
  # G = library.Grid(x=20, y=20)
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:] + [invals[0]]):
     candidates.append((size(a, b), a, b))
    #  G.overlays[tuple(a)] = 'X'
  candidates = sorted(candidates, reverse=False)
  # G.overlays[(2,3)] = 't'
  # G.overlays[(2,1)] = 'f'
  # print(G)
  for rect_size, a, b in candidates:
    if rect_size > 1870800075: continue
    if unimpeded(a, b, vectors):
      print(rect_size, a, b)
      # return rect_size, a, b

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "9")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
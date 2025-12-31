#!/usr/bin/env python3
import puzzle, library
import numpy as np

def parse_input(INPUT):
  return [list(library.ints(l)) for l in INPUT]

def one(INPUT):
  invals = parse_input(INPUT)
  vals = []
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
      vals.append(size(a, b))
  return max(vals)

def size(a, b):
  return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1]) + 1)

def maxes(loc_a, loc_b):
  max_x = max(loc_a[0], loc_b[0])
  max_y = max(loc_a[1], loc_b[1])
  min_x = min(loc_a[0], loc_b[0])
  min_y = min(loc_a[1], loc_b[1])
  return (min_x, min_y, max_x, max_y)

def buffer_polygon(points, val):
  out = []
  for i in range(len(points)):
    prev_i = (i - 1) % len(points)
    next_i = (i + 1) % len(points)
    prev_x, prev_y = points[prev_i]; cur = points[i]; next_x, next_y = points[next_i]
    n = prev_y > next_y; s = not n
    e = prev_x < next_x; w = not e
    if n and e: # nw
      out.append(((cur[0] - val ), (cur[1] - val)))
    elif n and w: # sw
      out.append(((cur[0] - val ), (cur[1] + val)))
    elif s and e: # ne
      out.append(((cur[0] + val ), (cur[1] - val)))
    elif s and w: # se
      out.append(((cur[0] + val ), (cur[1] + val)))
    else: print("ERROR")
  return out

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

X, Y = 0, 1

# TODO unit tests for within
def within(pt, vectors):
  # from 0, pt_y to pt
  vectors = sorted(vectors, key=lambda a: a[0][0])
  lines = [vect for vect in vectors if intersect((0, pt[1]), pt, vect[0], vect[1])]
  active = False; last_active = -1
  for l in lines:
    if l[0][1] < l[1][1]:
      active = True
    else:
      last_active = l[0][0]
      active = False
  return active or pt[0] == last_active

def covers(rect, poly_path):
  min_x, min_y, max_x, max_y = maxes(*rect)
  # corners = within((min_x, min_y), poly_path) and within((min_x, max_y), poly_path) and within((max_x, max_y), poly_path) and within((max_x, max_y), poly_path)
  # if not corners: return False

  # sides such that within the rect is to the right
  sides = [((min_x, min_y), (max_x, min_y)),  # top
            ((max_x, min_y), (max_x, max_y)),  # right
            ((max_x, max_y), (min_x, max_y)), # bottom
            ((min_x, max_y), (min_x, min_y)), # left
          ]
  for c, d in poly_path:
    for a, b in sides:
      if orient(a, b, c) <= 0 and orient(a, b, d) > 0:
        ns = a[1] != b[1]; ew = not ns
        if ns and min_y < c[1] < max_y:
          # print(f"bailing {maxes(*rect)} due to {a, b, c, d}")
          # print(f"orient({a}, {b}, {c}) {orient(a, b, c)}")
          # print(f"orient({a}, {b}, {d}) {orient(a, b, d)}")
          return False
        elif ew and min_x < c[0] < max_x:
          # print(f"bailing {maxes(*rect)} due to {a, b, c, d}")
          # print(f"orient({a}, {b}, {c}) {orient(a, b, c)}")
          # print(f"orient({a}, {b}, {d}) {orient(a, b, d)}")
          return False
  # for p1, p2 in poly_path:
  #   if p1[Y] <= min_y < p2[Y] and min_x < p1[X] < max_x: # top
  #     return False
  #   if p2[Y] < max_y <= p1[Y] and min_x < p1[X] < max_x: # bottom
  #     return False
  #   if p1[X] <= min_x < p2[X] and min_y < p1[Y] < max_y: # left
  #     return False
  #   if p2[X] < min_x <= p1[X] and min_y < p1[Y] < max_y: # right
  #     return False
    
  return True

def two(INPUT):
  invals = parse_input(INPUT)
  buffered = [(iv[0] + 0.5, iv[1] + 0.5) for iv in invals]
  buffered = buffer_polygon(buffered, 0.5)
  poly_path = list(zip(buffered, buffered[1:] + [buffered[0]]))

  candidates = []
  # print(poly_path)
  # G = library.Grid(20, 20)
  # for a, b in poly_path:
  #   G.overlays[a] = 'X'
  # print(G)
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
     candidates.append((size(a, b), a, b))
  candidates = sorted(candidates, reverse=True)

  # candidates = [(0, (2, 3), (10,6))]
  for _, a, b in candidates:
    if covers((a, b), poly_path):
      print(a, b)
      return size(a, b)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "9")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

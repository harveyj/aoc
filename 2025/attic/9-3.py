#!/usr/bin/env python3
import puzzle, library, collections
import numpy as np
from itertools import chain

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

X,Y = 0, 1

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

def vector_overlap(segment, vectors):
  return [vect for vect in vectors if intersect(segment[0], segment[1], vect[0], vect[1])]

def dump(xs, untiled, invals, S=(0,0), E=(0,0)):
  G = library.Grid(x=25, y=25)
  for x in xs:
    for segment in untiled[x]:
      for y in range(*segment):
        G.overlays[(x, y)] = 'u'
  for iv in invals:
    G.overlays[tuple(iv)] = 'X'
  G.overlays[S] = 'S'
  G.overlays[E] = 'E'
  
  print(G)

def dump2(invals, pt1, pt2):
  G = library.Grid(x=30, y=30)
  for iv in invals:
    G.overlays[tuple(iv)] = 'X'
  G.overlays[tuple(pt1)] = '1'
  G.overlays[tuple(pt2)] = '2'
  print(G)

def check(a, b, xs, untiled):
  # grab the bounding box
  (min_x, min_y, max_x, max_y) = maxes(a, b)
  for x in xs:
    # intersect it with the set of line segments that are untiled
    if x < min_x or x > max_x: continue
    for untiled_ys in untiled[x]:
      if min_y <= untiled_ys[0] < max_y or min_y <= untiled_ys[1] < max_y:
        return False
  return True


def two(INPUT):
  invals = parse_input(INPUT)
  invals.reverse() # reverse chirality lol
  MIN = 0; MAX_Y = max(pt[Y] for pt in invals) + 2

  raw_xs = [inval[0] for inval in invals]
  # need to go one over as well
  raw_x_adj = [x+1 for x in raw_xs]
  xs = sorted(list(set(raw_xs+raw_x_adj)))
  vectors = list(zip(invals, invals[1:] + [invals[0]]))
  # get all crosses
  horiz = sorted([v for v in vectors if v[0][X] != v[1][X]], key=lambda a: a[0][1])
  untiled = collections.defaultdict(list) # closed, open range
  # foreach x: scan that x figuring out where that line is either tiled or untiled
  for x in xs: # xs
    # get all vectors that intersect with (x, 0) --> (x, MAX)
    crosses = vector_overlap(((x, MIN), (x, MAX_Y)), horiz)
    prev = 0 # where to start the untiled segment from
    active = False
    for cross in crosses:
      if cross[0][X] < cross[1][X]: # l-r = start
        if not active:
          untiled[x].append((prev, cross[0][Y]))
        prev = cross[1][Y] + 1
        active = True
      else: # r-l = end, and it has to extend past 
        if cross[1][X] < x: active = False
        prev = cross[1][Y] + 1
    untiled[x].append((prev, MAX_Y))
    # print(f"x{x} crosses {crosses} untiled {untiled[x]}")
  print('done tracing')
  # dump(xs, untiled, invals)
  candidates = []
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
     candidates.append((size(a, b), a, b))
  candidates = sorted(candidates, reverse=True)

  for rect_size, a, b in candidates:
    if check(a, b, xs, untiled):
      # dump(xs, untiled, invals, S=tuple(a), E=tuple(b))
      return rect_size, a, b
      pass

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "9")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

  # # 2252271894 too high

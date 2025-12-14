#!/usr/bin/env python3
import puzzle, re, library

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

def active(pt, green_right, green_left, green_up, green_down):
  x, y = pt
  is_active = False
  if pt in green_right or pt in green_left or pt in green_up or pt in green_down: return True
  for xi in range(0, x):
    if (xi, y) in green_right:
      is_active = True
    elif (xi, y-1) in green_left:
      is_active = False
  return is_active

def size(a, b):
  return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1]) +1)

def maxes(loc_a, loc_b):
  max_x = max(loc_a[0], loc_b[0])
  max_y = max(loc_a[1], loc_b[1])
  min_x = min(loc_a[0], loc_b[0])
  min_y = min(loc_a[1], loc_b[1])
  return (min_x, min_y, max_x, max_y)

def check(a, b, actives):
  (min_x, min_y, max_x, max_y) = maxes(a, b)
  for x in range(min_x, max_x):
    if not (x, min_y) in actives or not (x, max_y in actives): return False
  for y in range(min_y, max_y):
    if not (min_x, y) in actives or not (max_x, y in actives): return False
  return True

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

def two(INPUT):
  invals = parse_input(INPUT)
  MIN = 0; MAX_X = max([pt[X]] for pt in invals); MAX_Y = max([pt[Y]] for pt in invals)

  # green_right = {}
  # green_left = {}
  # green_up = {}
  # green_down = {}
  # for loc_a, loc_b in zip(invals, invals[1:] + [invals[0]]):
  #   (min_x, min_y, max_x, max_y) = maxes(loc_a, loc_b)
  #   if min_x != max_x:
  #     if loc_a[0] < loc_b[0]:
  #       for x in range(min_x, max_x+1):
  #         green_down[(x, min_y)] = True
  #     else:
  #       for x in range(min_x, max_x+1):
  #         green_up[(x, min_y)] = True
  #   else:
  #     if loc_a[1] < loc_b[1]:
  #       for y in range(min_y, max_y+1):
  #         green_left[(min_x, y)] = True
  #     else:
  #       for y in range(min_y, max_y+1):
  #         green_right[(min_x, y)] = True


  xs = set([inval[0] for inval in invals])
  ys = set([inval[1] for inval in invals])
  vectors = list(zip(invals, invals[1:] + [invals[0]]))

  actives = {}
  for x in xs:
    active = False
    for y in range(0, 100000):
      if (x, y) in green_left or (x, y) in green_right:
        actives[(x, y)] = '@'
      if (x, y-1) in green_up:
        active = False
      if (x, y) in green_down:
        active = True
      if active: actives[(x, y)] = '@'

  # for y in ys:
  #   active = False
  #   for x in range(0, 100000):
  #     if (x, y) in green_up or (x, y) in green_down:
  #       actives[(x, y)] = '@'
  #     if (x-1, y) in green_left:
  #       active = False
  #     if (x, y) in green_right:
  #       active = True
  #     if active: actives[(x, y)] = '@'

  print('done tracing')
  candidates = []
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
     candidates.append((size(a, b), a, b))
  candidates = sorted(candidates, reverse=False)
  max_size = 0
  for rect_size, a, b in candidates:
    # print('.', end='')
    good = check(a, b, actives)
    if good: 
      if rect_size > max_size:
        max_size = rect_size
        print('new max', rect_size)


if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "9")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

  # # 2252271894 too high
      4643767804
      4602912072
      2317752927
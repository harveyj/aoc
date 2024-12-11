#!/usr/bin/env python3
import puzzle, library
from library import pt_add

def parse_input(INPUT):
  return [l.split() for l in INPUT]

dir_map = {'U': (0, -1), 
           'D': (0, 1), 
           'L': (-1, 0), 
           'R': (1, 0), 
           }
corner_map = {('L', 'U'): 'L',
              ('L', 'D'): 'F',
              ('R', 'U'): 'J',
              ('R', 'D'): '7',
              ('U', 'R'): 'F',
              ('U', 'L'): '7',
              ('D', 'R'): 'L',
              ('D', 'L'): 'J',
              }


def find_start(G):
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == 'S':
        return (x, y)

# Identical to seen from 10
def seen(G):
  S = find_start(G)
  loc = S
  seen = set()
  start_code = ''
  dirs = {'-': ((-1, 0), (1, 0)), '|': ((0, 1), (0, -1)), 'F': ((1, 0), (0, 1)), 'J': ((-1, 0), (0, -1)),'7': ((-1, 0), (0, 1)),'L': ((1, 0), (0, -1)),}
  while len(seen) == 0 or loc != S:
    code = G.get(loc)
    # print(loc, code, len(seen))
    if code == 'S':
      seen.add(loc)
      legal_left, legal_up, legal_right, legal_down = False, False, False, False
      if G.get(pt_add(loc, (-1, 0))) in ['F', 'L', '-']: 
        legal_left = True
      if G.get(pt_add(loc, (1, 0))) in ['7', 'J', '-']:
        legal_right = True
      if G.get(pt_add(loc, (0, -1))) in ['F', '7', '|']: 
        legal_up = True
      if G.get(pt_add(loc, (0, 1))) in ['J', 'L', '|']:
        legal_down = True
      if legal_left and legal_up: start_code = 'J'
      if legal_left and legal_right: start_code = '-'
      if legal_left and legal_down: start_code = '7'
      if legal_up and legal_down: start_code = '|'
      if legal_right and legal_up: start_code = 'L'
      if legal_right and legal_down: start_code = 'F'
      code = start_code
    dir = dirs[code]
    for d in dir:
      if pt_add(loc, d) == S and len(seen) > 3: # ugh
         return seen, start_code
    x, y = pt_add(loc, dir[0])
    if (x, y) in seen:
      x, y = pt_add(loc, dir[1])
    if (x, y) in seen:
      print('ERROR', x, y, )
    loc = (x, y)
    seen.add(loc)


def one(INPUT):
  instrs = parse_input(INPUT)
  
  G = library.Grid(x=500, y=400)
  sx, sy = 125, 250
  prev_dir = 'U'
  for dir, mag, color in instrs:
    dx, dy = dir_map[dir]
    dx *= int(mag); dy *= int(mag)
    G.set((sx, sy), corner_map[(prev_dir, dir)])

    if dir in ['U', 'D']:
      for y in range(min(sy+1, sy+dy), max(sy, sy+dy)):
        G.set((sx, y), '|')
    if dir in ['L', 'R']:
      for x in range(min(sx+1, sx+dx), max(sx, sx+dx)):
        G.set((x, sy),  '-')
    sx, sy = sx+dx, sy+dy
    prev_dir = dir
  G.set((sx, sy), 'S')
  # for dy in range(2):
  #   for dx in range(2):
  #     print(G.window(dx*250, dy*250, (dx+1)*250, (dy+1)*250))
  #     print('')


  L, start_code = seen(G)
  enclosed = set()
  toggles = set()
  for y in range(G.max_y()):
    in_loop = False
    x = -1
    while x < G.max_x():
      num_up, num_down = 0, 0
      x += 1
      if (x, y) in L:
        while x < G.max_x():
          code = G.get((x, y))
          if code == 'S': code = start_code
          if code in ['|', 'L', 'J']: num_up += 1
          if code in ['|', 'F', '7']: num_down += 1
          if num_up + num_down == 2:
            if num_up == num_down == 1:
              in_loop = not in_loop
              toggles.add((x, y))
            break
          x += 1

      elif in_loop:
        enclosed.add((x, y))
  for pt in enclosed: G.overlays[pt] = 'T'
  # print(G)
  lengths = [int(instr[1]) for instr in instrs]
  return len(enclosed) + sum(lengths)

  out = 0
  return out

def find_nte(array, val):
  # print('nte', array, val)
  if len(array) == 0:
    return -1
  if array[-1] <= val:
    return len(array) - 1
  for i in range(len(array) - 1):
    if array[i] < val < array[i+1]:
      return i
  return -1

def contained(pt, segments, up_xes, down_xes):
  x, y = pt
  latest_u = find_nte(up_xes, x)
  latest_d = find_nte(down_xes, x)
  for p1, p2 in segments:
    max_x = max(p1[0], p2[0])
    max_y = max(p1[1], p2[1])
    min_x = min(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    if min_x <= x <= max_x and min_y <= y <= max_y:
      return True
  if latest_u == -1:
    return False
  if latest_d == -1:
    return True
  if up_xes[latest_u] > down_xes[latest_d]: 
    return True
  return False

def bounded(seg, val, dim='x'):
  idx = 0 if dim == 'x' else 1
  max_v = max(seg[0][idx], seg[1][idx])
  min_v = min(seg[0][idx], seg[1][idx])
  return min_v <= val <= max_v

def two(INPUT):
  DEBUG = False
  instrs = parse_input(INPUT)
  
  segments = {'U': [],
              'D': [],
              'L': [],
              'R': [],
  }
  G=library.Grid(x=40,y=20)
  pt = 10,10
  instrs = [('LDRU'[int(color[-2])], int(color[2:-2], 16)) for (dir, mag, color) in instrs]
  for dir, mag in instrs:
    delta = library.mul_vect(dir_map[dir], mag)
    new_pt = library.pt_add(pt, delta)
    if dir in ['U', 'L']:
      segments[dir].append((new_pt, pt))
    else:
      segments[dir].append((pt, new_pt))
    pt = new_pt
  all_segments = [seg for dir in 'RDLU' for seg in segments[dir]]
  all_x = sorted(set([seg[0][0] for seg in all_segments] + [seg[0][0]+1 for seg in all_segments]))
  all_y = sorted(set([seg[0][1] for seg in all_segments] + [seg[0][1]+1 for seg in all_segments]))
  
  for key in 'UD': segments[key] = sorted(segments[key], key=lambda a: a[0])
  for key in 'RL': segments[key] = sorted(segments[key], key=lambda a: a[0])
  # reverse chirality
  if min([seg[0] for seg in segments['D']]) < min([seg[0] for seg in segments['U']]) :
    tmp = segments['U']
    segments['U'] = segments['D']
    segments['D'] = tmp
  # print(segments)
  out = 0
  for y, y2 in zip(all_y, all_y[1:]):
    up_xes = [seg[0][0] for seg in segments['U'] if bounded(seg, y, dim='y')]
    down_xes = [seg[0][0] for seg in segments['D'] if bounded(seg, y, dim='y')]
    if DEBUG: print('\nCONSIDERING ROW', (y, y2))
    row_total = 0
    for x, x2 in zip(all_x, all_x[1:]):
      if DEBUG: print('\nCONSIDERING CELL', (x, x2))

      if (contained((x, y), all_segments, up_xes, down_xes)):
        if DEBUG: 
          # for ox in range(x, x2):
          #   for oy in range(y, y2):
          #     G.overlays[(ox, oy)]= 'x'
          print((x2 - x) * (y2 - y))
        out += (x2 - x) * (y2 - y)
        row_total += (x2 - x) * (y2 - y)

    if DEBUG: print('rt', row_total)
    row_total = 0
  if DEBUG: 
    for pt1, pt2 in segments['U']:
      for y in range(pt1[1], pt2[1]):
        G.overlays[(pt1[0], y)] = 'u'
    for pt1, pt2 in segments['D']:
      for y in range(pt1[1], pt2[1]):
        G.overlays[(pt1[0], y)] = 'd'
    for pt1, pt2 in segments['R']:
      for x in range(pt1[0], pt2[0]):
        G.overlays[(x, pt1[1])] = 'r'
    for pt1, pt2 in segments['L']:
      for x in range(pt1[0], pt2[0]):
        G.overlays[(x, pt1[1])] = 'l'

  if DEBUG: print(G)
  return out

# #3 = 8 (8 outer 0 inner)
# #4 = 9 (2x2) (8 outer 1 inner)
# #5 = 62 (example) (38 outer 24 inner)
# #6 = 16 (3x3) (12 out 4 in)
# #7 = 15 (3x3 carveout) (12 out 3 in)
# #8 = custom (67)
# #9 = custom (reverse chirality, emulate example)
if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "18")

  p.run(one, 0) 
  p.run(two, 0) 

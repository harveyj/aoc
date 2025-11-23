#!/usr/bin/env python3
import re, puzzle, copy, collections

def one(INPUT):
  marked = {}
  for l in INPUT:
    match = re.search(r"(.*) .=(.*)\.\.(.*),.=(.*)\.\.(.*),.=(.*)\.\.(.*)", l) #"
    sig = 1 if match.group(1) == 'on' else 0
    x1, x2, y1, y2, z1, z2 = map(int, match.group(2, 3, 4, 5, 6, 7))
    x1 = max(x1, -50)
    x2 = min(x2, 50)
    y1 = max(y1, -50)
    y2 = min(y2, 50)
    z1 = max(z1, -50)
    z2 = min(z2, 50)
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        for z in range(z1, z2+1):
          marked[(x, y, z)] = sig
  return len(list(filter(lambda a: a, marked.values())))

# https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hpmgqn5/ 
# "if the cubes still overlap, split the cube by an axis into two"

def two(INPUT):
  X, Y, Z = range(3)

  def lower_left_in(cube1, pt):
    c11, c12 = cube1
    x_int = c11[X] <= pt[X] < c12[X]
    y_int = c11[Y] <= pt[Y] < c12[Y] 
    z_int = c11[Z] <= pt[Z] < c12[Z] 
    return x_int and y_int and z_int

  def volume(p1, p2):
    return (p2[0]-p1[0]) * (p2[1]-p1[1]) * (p2[2]-p1[2])
  def disjoint(c1, c2):
    return (c2[1][0] <= c1[0][0] or 
            c2[0][0] >= c1[1][0] or 
            c2[1][1] <= c1[0][1] or 
            c2[0][1] >= c1[1][1] or 
            c2[1][2] <= c1[0][2] or 
            c2[0][2] >= c1[1][2])
  def within(c1, c2):
    return (c1[0][0] <= c2[0][0] <= c2[1][0] <= c1[1][0] and
            c1[0][1] <= c2[0][1] <= c2[1][1] <= c1[1][1] and
            c1[0][2] <= c2[0][2] <= c2[1][2] <= c1[1][2])

  def parse_cube(l):
    match = re.search(r"(.*) .=(.*)\.\.(.*),.=(.*)\.\.(.*),.=(.*)\.\.(.*)", l) #"
    new_is_on = match.group(1) == 'on'
    x1, x2, y1, y2, z1, z2 = list(map(int, match.group(2, 3, 4, 5, 6, 7)))
    new_cube = [[x1, y1, z1], [x2+1, y2+1, z2+1]]
    return new_is_on, new_cube
  
  # if c2 partially overlaps c1, split c2 along an axis such that all of 
  # c2 along that axis overlaps, or doesn't
  def split_cube(c1, c2):
    c1_x1, c1_y1, c1_z1 = c1[0]; c1_x2, c1_y2, c1_z2 = c1[1]
    c2_x1, c2_y1, c2_z1 = c2[0]; c2_x2, c2_y2, c2_z2 = c2[1]
    v = []
    if c2_x1 < c1_x2 < c2_x2:
      split_axis = 0; v = [c2_x1, c1_x2, c2_x2]
    elif c2_x1 < c1_x1 < c2_x2:
      split_axis = 0; v = [c2_x1, c1_x1, c2_x2]
    elif c2_y1 < c1_y2 < c2_y2:
      split_axis = 1; v = [c2_y1, c1_y2, c2_y2]
    elif c2_y1 < c1_y1 < c2_y2:
      split_axis = 1; v = [c2_y1, c1_y1, c2_y2]
    elif c2_z1 < c1_z2 < c2_z2:
      split_axis = 2; v = [c2_z1, c1_z2, c2_z2]
    elif c2_z1 < c1_z1 < c2_z2:
      split_axis = 2; v = [c2_z1, c1_z1, c2_z2]
    if v:
      ret_1 = copy.deepcopy(c2); ret_2 = copy.deepcopy(c2)
      ret_1[0][split_axis] = v[0]
      ret_1[1][split_axis] = v[1]
      ret_2[0][split_axis] = v[1]
      ret_2[1][split_axis] = v[2]
      return ret_1, ret_2
    print('ERROR NO SPLIT', c1, c2)

  cubes = [parse_cube(l) for l in INPUT]
  total_vol = 0
  # Go backwards through the cubes
  cubes.reverse()
  # invariant: disjoints contains cuboids that are mutually non-overlapping
  disjoints = []

  for (c_on, cube) in cubes:
    in_fragments = [cube]
    # break it down until it is entirely either within
    # cubes in seen, or disjoint from cubes in seen.
    # anything entirely disjoint goes in processed, anything entirely
    # occluded gets dropped
    processed = [] # segments which are entirely disjoint
    while in_fragments:
      # invariant is that the volume covered by in_fragments 
      # decreases monotonically
      # you split it - area stays same but is sliced thinner
      # first fragment within a prior segment - drop it
      # first fragment entirely disjoint - drop it (add it to disjoints)
      frag = in_fragments.pop(0)
      tainted = False
      for dj in disjoints:
        if within(dj, frag): 
          tainted = True
          break
        if not disjoint(dj, frag):
          reg_1, reg_2 = split_cube(dj, frag)
          tainted = True
          if not within(dj, reg_1):
            in_fragments.append(reg_1)
          if not within(dj, reg_2):
            in_fragments.append(reg_2)
          break
      if not tainted: processed.append(frag)
    if c_on: 
      total_vol += sum([volume(*p) for p in processed])
    disjoints.extend(processed)
  
  return total_vol

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "22")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

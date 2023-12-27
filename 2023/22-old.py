#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  def parse_line(l):
    a, b = l.split('~')
    return tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))
  lines = [parse_line(l) for l in INPUT.split('\n')]
  return [(*line, i) for i, line in enumerate(lines)]

def advance(cube):
  x1, y1, z1 = cube[0]
  x2, y2, z2 = cube[1]
  return (x1, y1, z1-1), (x2, y2, z2-1), cube[2]


def overlap(cube1, cube2):
  x1, y1, z1 = cube1[0]
  x2, y2, z2 = cube1[1]
  a1, b1, c1 = cube2[0]
  a2, b2, c2 = cube2[1]
  return not ((a2 < x1 or a1 >= x2+1) or (b2 < y1 or b1 >= y2+1) or (c2 < z1 or c1 >= z2+1))

def bottom(cube):
  return cube[1][2]  # z2

def descend(cubes, adjacents):
  def legal_descend(new_cube, seen_cubes):
    if bottom(new_cube) < 1: return False
    for sc in seen_cubes:
      if overlap(new_cube, sc): return False
    return True
  # cubes = sorted(cubes, key=bottom)
  seen_cubes = []
  for i, cube in enumerate(cubes):
    new_cube = advance(cube)
    if legal_descend(new_cube, seen_cubes):
      seen_cubes.append(new_cube)
    else: seen_cubes.append(cube)
  return sorted(seen_cubes, key=bottom)



def test(INPUT):
  pass
  # print("t", overlap(((0, 0, 1), (0, 0, 1)), ((0,0,1), (0,0,1))))
  # print('f', overlap(((0, 0, 1), (0, 0, 1)), ((1,0,1), (1,0,1))))
  # print('t', overlap(((1, 0, 1), (1, 2, 1)), ((0, 0, 1), (2, 0, 1))))


def one_b(INPUT):
  cubes = parse_input(INPUT)
  cubes = sorted(cubes, key=bottom)
  new_cubes = descend(cubes)
  cubes = None
  while cubes != new_cubes:
    cubes = new_cubes
    new_cubes = descend(cubes)
  out = 0
  for i in range(len(cubes)):
    stack_edited = cubes[:i] + cubes[i+1:]
    descend_stack = descend(stack_edited)
    if descend_stack == stack_edited: out += 1 

  return out



def descend2(cubes):
  def legal_descend(new_cube, seen_cubes):
    if bottom(new_cube) < 1: return False
    for sc in seen_cubes[::-1]:
      if overlap(new_cube, sc): return False
    return True
  seen_cubes = []
  for cube in cubes:
    new_cube = cube
    while legal_descend(new_cube, seen_cubes):
      cube = new_cube
      new_cube = advance(cube)
    seen_cubes.append(cube)
  return seen_cubes


def one(INPUT):
  cubes = parse_input(INPUT)
  cubes = sorted(cubes, key=bottom)
  cubes = descend2(cubes)
  out = 0
  for i in range(len(cubes)):
    print('.', end='')
    stack_edited = cubes[:i] + cubes[i+1:]
    descend_stack = descend2(stack_edited)
    if descend_stack == stack_edited: out += 1

  # grid = puzzle.Grid(x=30, y=20)
  # for y in range(30):
  #   for z in range(20):
  #     cell = ((0, y, z), (100, y, z))
  #     for c in cubes:
  #       if overlap(cell, c):
  #         grid.overlays[(y, 20-z)] = 'ABCDEFGH'[c[2]]
  # print(grid)


  return out


def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

p = puzzle.Puzzle("22")
p.run(one, 0)
# p.run(two, 0)

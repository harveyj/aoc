#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  trees= [list(map(int, list(l))) for l in INPUT]
  return trees

def one(INPUT):
  trees = parse(INPUT)
  seen = set()
  print(trees)
  for dx, x_start in [(1, 0), (-1, len(trees[0])-1)]:
    for y in range(len(trees)):
      max = -1
      x = x_start
      while 0 <= x < len(trees[0]):
        if trees[y][x] > max:
          max = trees[y][x]
          seen.add((x, y))
        x += dx
  
  for dy, y_start in [(1, 0), (-1, len(trees)-1)]:
    for x in range(len(trees[0])):
      max = -1
      y = y_start
      while 0 <= y < len(trees):
        if trees[y][x] > max:
          max = trees[y][x]
          seen.add((x, y))
        y += dy

  return len(seen)

def two(INPUT):
  def all_visible(x, y):
    iters = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    seen = []
    for dx, dy in iters:
      nx, ny = x+dx, y+dy
      dir_seen = 0
      # print(dx, dy, x, y, nx, ny)
      # print('orig', trees[y][x], 'new', trees[ny][nx])
      while 0 <= nx < len(trees[0]) and 0 <= ny < len(trees):
        dir_seen += 1
        # print(dx, dy, x, y, nx, ny)
        # print('orig', trees[y][x], 'new', trees[ny][nx])
        if trees[y][x] <= trees[ny][nx]: break
        nx += dx
        ny += dy
      seen.append(dir_seen)
    return seen

  trees = parse(INPUT)
  max = 0
  score = 0
  for x in range(len(trees[0])):
    for y in range(len(trees)):
      seen = all_visible(x, y)
      score = seen[0] * seen[1] * seen[2] * seen[3]
      if score > max:
        max = score
  return max

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "8")

  p.run(one, 0) 
  p.run(two, 0) 

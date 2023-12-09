#!/usr/bin/env python3
import puzzle

def one(INPUT):
  out = 0
  G = puzzle.Grid(grid=INPUT.split('\n'))
  print(G)
  legal_neighbors = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',]

  for y in range(G.max_y()):
    num = 0
    sym = False
    for x in range(G.max_x()):
      c = G.get((x, y))
      if c.isdigit():
        num = num * 10 + int(c)
        neighbors = [ n for n in G.neighbors_diag((x, y))
                      if n not in legal_neighbors ]
        if len(neighbors) > 0:
          print(neighbors)
          sym = True
      else:
        if sym:
          out += num
        elif num > 0:
          print('filtering', num)
        num = 0
        sym = False
    if sym:
      out += num
    elif num > 0:
      print('filtering', num)

  return out

def two(INPUT):
  G = puzzle.Grid(grid=INPUT.split('\n'))
  gear_nums = dict()
  for y in range(G.max_y()):
    num = 0
    gears = set()
    for x in range(G.max_x()):
      c = G.get((x, y))
      if c.isdigit():
        num = num * 10 + int(c)
        gears.update([loc for loc in G.neighbors_diag_locs((x, y)) if G.get(loc) == '*'])
      else:
        for g in gears:
          ngn = gear_nums.get(g, [])
          gear_nums[g] = ngn + [num]
        num = 0
        gears = set()

    if num:
      for g in gears:
        # danger
        gear_nums[g] += [num]

  out = 0
  for g in gear_nums.values():
    print(g)
    if len(g) == 2:
      out += g[0] * g[1]
  return out

p = puzzle.Puzzle("3")
p.run(one, 0)
p.run(two, 0)

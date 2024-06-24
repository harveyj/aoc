#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

WEPS = '''Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0'''

ARM = '''None 0 0 0
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5'''

RING = '''None 0 0 0
D+1    25     1       0
D+2    50     2       0
D+3   100     3       0
Def+1   20     0       1
Def+2   40     0       2
Def+3   80     0       3'''

def parse(block):
  return [(line.split()[0], list(map(int, line.split()[1:4]))) for line in block.split("\n")]


def one(INPUT):
  weps = parse(WEPS)
  arm = parse(ARM)
  ring = parse(RING)
  # sim(8, 1)
  # return 0
  for w, wstats in weps:
    for a, astats in arm:
      for r, rstats in ring:
        for r2, r2stats in ring:
          # print(wstats, astats, rstats)
          h_a = wstats[1] + rstats[1] + r2stats[1]
          h_d = astats[2] + rstats[2] + r2stats[2]
          cost = wstats[0]+astats[0]+rstats[0]+r2stats[0]
          if cost < 91 and sim(h_a, h_d):
            print(w, a, r, r2, cost, h_a, h_d)

def two(INPUT):
  weps = parse(WEPS)
  arm = parse(ARM)
  ring = parse(RING)
  for w, wstats in weps:
    for a, astats in arm:
      for r, rstats in ring:
        for r2, r2stats in ring:
          # print(wstats, astats, rstats)
          h_a = wstats[1] + rstats[1] + r2stats[1]
          h_d = astats[2] + rstats[2] + r2stats[2]
          cost = wstats[0]+astats[0]+rstats[0]+r2stats[0]
          if cost > 135 and not sim(h_a, h_d):
            print(w, a, r, r2, cost, h_a, h_d)


def sim(h_a, h_d):
  b_hp, b_a, b_d = 104, 8, 1
  h_hp = 100
  while b_hp > 0 and h_hp > 0:
    b_hp -= max((h_a - b_d), 1)
    # print('b_hp', b_hp)
    if b_hp <= 0: break
    h_hp -= max((b_a - h_d), 1)
    # print('h_hp', h_hp)
  # print(b_hp, h_hp)
  return b_hp < h_hp


p = puzzle.Puzzle("13")
# p.run(one, 0)
p.run(two, 0)

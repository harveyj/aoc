#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import collections

def parse(INPUT):
  pat = re.compile('(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()


def one(INPUT):
  total_t = 2503
  reindeer = parse(INPUT)
  for r in reindeer:
    dist, fly_t, rest_t = int(r[1]), int(r[2]), int(r[3])
    # print(fly_t, rest_t)
    cycle_t = fly_t + rest_t
    cycles = total_t // cycle_t
    rem = total_t % cycle_t
    rem = min(fly_t, rem)
    # print(cycles, cycle_t, rem, fly_t)
    print(r[0], cycles*fly_t*dist + rem*dist)
  return 0

# there was an off by one somewhere in there...
def two(INPUT):
  total_t = 2503
  reindeer = list(parse(INPUT))
  r_dists = dict()
  scores = collections.defaultdict(int)
  for r in reindeer:
    name = r[0]
    r_dists[name] = [0]
    for t in range(total_t):
      dist, fly_t, rest_t = int(r[1]), int(r[2]), int(r[3])
      cycle_t = fly_t + rest_t
      t_pos = t % cycle_t
      incr = dist if t_pos < fly_t else 0
      r_dists[name].append(r_dists[name][t] + incr)
  for t in range(1, total_t):
    dists = {r : r_dists[r][t] for r in r_dists.keys()}
    max_score = max(dists.values())
    # print(t, reindeer)
    for r in reindeer:
      print(r)
      if r_dists[r[0]][t] == max_score: scores[r] += 1
  print(scores)
  return 0
p = puzzle.Puzzle("14")
# p.run(one, 0)
p.run(two, 0)

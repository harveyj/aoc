#!/usr/bin/env python3
import puzzle
import re
import collections

def parse(INPUT):
  pat = re.compile('(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
  for l in INPUT:
    yield re.match(pat, l).groups()

def one(INPUT):
  total_t = 2503
  reindeer = parse(INPUT)
  score_max = 0
  for r in reindeer:
    dist, fly_t, rest_t = int(r[1]), int(r[2]), int(r[3])
    cycle_t = fly_t + rest_t
    cycles = total_t // cycle_t
    rem = total_t % cycle_t
    rem = min(fly_t, rem)
    score = cycles*fly_t*dist + rem*dist
    if score > score_max:
      score_max = score
  return score_max

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
    for r in reindeer:
      if r_dists[r[0]][t] == max_score: scores[r] += 1
  # print(scores)
  return max(scores.values())

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "14")

  p.run(one, 0)
  p.run(two, 0)

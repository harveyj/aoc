#!/usr/bin/env python3
import puzzle, re, collections, functools

def parse_input(INPUT):
  return library.Grid(raw=INPUT)

def all_reachable(G, n, S):
  queue = collections.deque([S])
  for _ in range(n):
    new_pts = set()
    while queue:
      pt = queue.pop()
      for new_pt in puzzle.neighbors(pt):
        if G.get_repeating(new_pt) == '.' and new_pt not in new_pts:
          new_pts.add(new_pt)
    queue = collections.deque(new_pts)
  return queue

def one(INPUT):
  G = parse_input(INPUT)
  S = G.detect('S')[0]
  G.set(S, '.')
  return len(all_reachable(G, 64, S))

def two(INPUT):
  G = parse_input(INPUT)
  S = G.detect('S')[0]
  G.set(S, '.')
  print([len(all_reachable(G, 65 + 131*i, S)) for i in range(3)])
  # plug the above into wolfram alpha to get a quadratic equation
  # plug in target - 65 // 131
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "21")

  p.run(one, 0) 
  p.run(two, 0) 

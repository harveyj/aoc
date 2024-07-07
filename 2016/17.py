#!/usr/bin/env python3
import puzzle, library
import re, hashlib, networkx as nx, collections

def md5hash(inval):
  md5_hash = hashlib.md5()
  md5_hash.update(inval.encode('utf-8'))
  return md5_hash.hexdigest()

LEGAL = 'bcdef'
def one(INPUT):
  salt = INPUT[0]
  queue = collections.deque()
  queue.append(('', (0,0)))
  G = library.Grid(x=4, y=4)
  num = 0
  good_paths = []
  while queue:
    path, loc = queue.popleft()
    num += 1
    # if num > 10: return
    if loc == (3,3):
      good_paths.append(path)
      continue
    inval = salt+path
    u_c, d_c, l_c, r_c = md5hash(inval)[:4]
    # print(u_c, d_c, l_c, r_c, LEGAL)
    # print(d_c in LEGAL)
    if u_c in LEGAL:
      dx, dy = 0, -1
      new_loc = (loc[0] + dx, loc[1] + dy)
      if G.get(new_loc):
        queue.append((path+'U', new_loc))
    if d_c in LEGAL:
      dx, dy = 0, 1
      new_loc = (loc[0] + dx, loc[1] + dy)
      if G.get(new_loc):
        queue.append((path+'D', new_loc))
    if l_c in LEGAL:
      dx, dy = -1, 0
      new_loc = (loc[0] + dx, loc[1] + dy)
      if G.get(new_loc):
        queue.append((path+'L', new_loc))
    if r_c in LEGAL:
      dx, dy = 1, 0
      new_loc = (loc[0] + dx, loc[1] + dy)
      if G.get(new_loc):
        queue.append((path+'R', new_loc))
    # print(queue)
  max_len = max([len(p) for p in good_paths])
  return max_len

def two(INPUT):
  return 0

p = puzzle.Puzzle("17")
p.run(one, 0)
# p.run(two, 0)

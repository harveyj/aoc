#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib
from collections import defaultdict

def one(INPUT):
  val = int(INPUT[0])
  buf = [0]
  cur_pos = 0
  steps = 2017
  for i in range(steps):
    cur_pos = (cur_pos + val) % len(buf) + 1
    buf.insert(cur_pos, i+1)
    # print(buf)
  idx = buf.index(2017)+1
  return buf[idx]

def two(INPUT):
  val = int(INPUT[0])
  buf = [0]
  cur_pos = 0
  steps = 50000
  post = None
  for i in range(steps):
    cur_pos = (cur_pos + val) % len(buf) + 1
    buf.insert(cur_pos, i+1)
    new_post = buf[buf.index(0) + 1]
    if post != new_post:
      print('new post', new_post)
      post = new_post
  cur_pos = 0
  steps = 50000001
  for i in range(steps):
    cur_pos = (cur_pos + val) % (i+1) + 1
    if cur_pos == 1:
      print('new post', i+1)


p = puzzle.Puzzle("2017", "17")
p.run(one, 0)
p.run(two, 0)
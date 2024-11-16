#!/usr/bin/env python3
import puzzle

def one(INPUT):
  total = 0
  for l in INPUT:
    l, w, h = list(map(int, l.split('x')))
    total += (l*w)*2 + (l*h)*2 + w*h*2
    total += min(l*w, l*h, w*h)
  return total

def two(INPUT):
  total = 0
  for l in INPUT:
    l, w, h = list(map(int, l.split('x')))
    total += l*w*h
    total += min((l+w)*2, (l+h)*2, (w+h)*2)
  return total

p = puzzle.Puzzle("2015", "2")
p.run(one, 0)
p.run(two, 0)

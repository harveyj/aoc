#!/usr/bin/env python3
import puzzle

def find_window(INPUT, length):
  window = list(INPUT[:length])
  for i in range(length, len(INPUT)):
    if len(set(window)) == length:
      return i
    window.append(INPUT[i])
    del window[0]
  return 0

def one(INPUT):
  return find_window(INPUT, 4)

def two(INPUT):
  return find_window(INPUT, 14)

p = puzzle.Puzzle("6")
p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle

def find_window(INPUT, length):
  for i in range(length, len(INPUT)):
    window = list(INPUT[i:i+length])
    if len(set(window)) == length:
      return i+length
  return 0

def one(INPUT):
  return find_window(INPUT[0], 4)

def two(INPUT):
  return find_window(INPUT[0], 14)

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "6")

  p.run(one, 0) 
  p.run(two, 0) 

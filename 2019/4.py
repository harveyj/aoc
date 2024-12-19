#!/usr/bin/env python3
import puzzle

def onetwo(INPUT, two=False):
  num=0
  a, b = map(int, INPUT[0].split('-'))
  for i in range(a, b):
    adjacent = []
    more_than_two = []

    is_adjacent = False
    is_inc = True
    prev = ''
    for c in str(i):
      if c == prev: 
        if c in adjacent:
          more_than_two.append(c)
        adjacent.append(c)

      if c < prev: is_inc = False
      prev = c

    if two:
      for char in adjacent:
        if char not in more_than_two: is_adjacent = True
    else:
      is_adjacent = len(adjacent) > 0
  
    if is_adjacent and is_inc: num += 1
  return num

def one(INPUT): return onetwo(INPUT, two=False)

def two(INPUT): return onetwo(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "4")
  p.run(onetwo, 0)
  p.run(two, 0)

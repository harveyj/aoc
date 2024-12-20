#!/usr/bin/env python3
import puzzle

def parse(INPUT):
  return [ord(c) - ord('a') for c in INPUT[0]]

FORBIDDEN = [ord('i') - ord('a'), ord('o') - ord('a'), ord('l') - ord('a')]

# Increment val in place
def increment(val):
  for i in range(len(val)):
    if val[i] in FORBIDDEN:
      val[i] = val[i] + 1
      for j in range(i+1, len(val)):
        val[j] = 0
  for i in range(len(val)-1, -1, -1):
    val[i] += 1
    if val[i] >= 26:
      val[i] = 0
    else:
      break

def check(val):
  def straight(val):
    for i in range(len(val) - 2):
      if val[i] == val[i+1] - 1 == val[i+2] - 2:
        return True
    return False
  def forbidden(val):
    for c in FORBIDDEN:
      if c in val: return False
    return True
  def pairs(val):
    pairs = set([pair for pair in zip(val, val[1:]) if pair[0] == pair[1]])
    return len(pairs) > 1
  return straight(val) and forbidden(val) and pairs(val)

def decode(val):
  return ''.join([chr(c + ord('a')) for c in val])

def one(INPUT):
  inval = parse(INPUT)
  limit = 0
  while True:
    limit += 1
    if check(inval): return decode(inval)
    increment(inval)

def two(INPUT):
  return puzzle.Puzzle("2015", "11").run(one, 1)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "11")

  p.run(one, 0) 
  p.run(two, 1)  # Two is just one with different input

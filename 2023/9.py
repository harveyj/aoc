#!/usr/bin/env python3
import puzzle

def parse_input(INPUT):
  return [list(map(int, l.split())) for l in INPUT]

def onetwo(INPUT):
  invals = parse_input(INPUT)
  trees = []
  for line in invals:
    allvals = []
    curvals = line
    while True:
      allvals.append(curvals)
      curvals = [curvals[i+1] - curvals[i] for i in range(len(curvals)-1)]
      if curvals.count(0) == len(curvals):
        break
    trees.append(allvals)

  out_1 = 0
  for t in trees:
    subtotal = 0
    for i in range(len(t)-1, -1, -1):
      subtotal += t[i][-1]
    out_1 += subtotal
  out_2 = 0
  for t in trees:
    subtotal = 0
    for i in range(len(t)-1, -1, -1):
      subtotal = t[i][0] - subtotal
    out_2 += subtotal

  return out_1, out_2

def one(INPUT):
  return onetwo(INPUT)[0]
def two(INPUT):
  return onetwo(INPUT)[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "9")

  p.run(one, 0) 
  p.run(two, 0) 

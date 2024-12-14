#!/usr/bin/env python3
import puzzle

def one(INPUT, two = False):
  OPENS = '<([{'; CLOSES = '>)]}'
  CORRECT_OPEN = dict(zip(CLOSES, OPENS))
  ONE_SCORES = {None: 0, ')': 3, ']': 57, '}': 1197, '>': 25137}
  TWO_SCORES = {None: 0, '(': 1, '[': 2, '{': 3, '<': 4}
  one_score = 0
  two_scores = []
  for l in INPUT:
    first_illegal = None
    stack = []
    for c in l:
      if c in CLOSES:
        match = stack.pop()
        if match != CORRECT_OPEN[c]:
          first_illegal = c
          break
      else:
        stack.append(c)
    one_score += ONE_SCORES[first_illegal]
    if not first_illegal:
      line_score = 0
      while stack:
        line_score *= 5
        line_score += TWO_SCORES[stack.pop()]
      two_scores.append(line_score)
  two_scores = sorted(two_scores)
  return two_scores[len(two_scores)//2] if two else one_score

two = lambda a: one(a, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "10")

  print(p.run(one, 0))
  print(p.run(two, 0))

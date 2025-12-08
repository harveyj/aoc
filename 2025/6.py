#!/usr/bin/env python3
import puzzle, library
import operator
import itertools

def parse_input(INPUT):
  return [library.ints(l) for l in INPUT[:-1]], INPUT[-1].split()

def one(INPUT):
  vals, opers = parse_input(INPUT)
  outs = []
  for i, o in enumerate(opers):
    op = operator.mul if o == '*' else operator.add
    outs.append(list(itertools.accumulate([row[i] for row in vals], func=op))[-1])
  return sum(list(outs))

def two(INPUT):
  sequences = []
  for i, _ in enumerate(INPUT[0]):
    col = [l[i] for l in INPUT]
    if col[-1] != " ":
      op = operator.mul if col[-1] == '*' else operator.add
      vals = []
    val = "".join(col[:-1])
    if val.strip() == "":
      sequences.append((op, vals))
    else:
      vals.append(int(val))
  sequences.append((op, vals))
  outs = []
  for op, vals in sequences:
    outs.append(list(itertools.accumulate(vals, func=op))[-1])

  return sum(outs)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "6")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

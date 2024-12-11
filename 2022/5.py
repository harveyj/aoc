#!/usr/bin/env python3
import puzzle
import re

def parse_line(l):
  pat = re.compile(r"move (\d+) from (\d+) to (\d+)")
  a, b, c = [int(i) for i in re.match(string=l, pattern=pat).groups()]
  return [a, b, c]

def parse(INPUT):
  stacks_raw, instrs_raw = '\n'.join(INPUT).split("\n\n")
  N_STACKS = (len(stacks_raw.split("\n")[-1])+1)//4
  stacks = [[] for i in range(N_STACKS)]
  for line in stacks_raw.split("\n")[-2::-1]:
    for i in range(N_STACKS):
      if line[1+i*4] != " ": stacks[i].append(line[1+i*4])
  instrs = [parse_line(l) for l in instrs_raw.split('\n')]
  return stacks, instrs

def one(INPUT):
  stacks, instrs = parse(INPUT)
  for n, fr, to in instrs:
    for i in range(n):
      stacks[to-1].append(stacks[fr-1].pop())

  return ''.join([s[-1] for s in stacks])

def two(INPUT):
  stacks, instrs = parse(INPUT)
  for n, fr, to in instrs:
    stacks[to-1] += list(stacks[fr-1][-n:])
    del(stacks[fr-1][-n:])
    # print(stacks)
  # print(stacks)
  return ''.join([s[-1] for s in stacks])

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "5")

  p.run(one, 0) 
  p.run(two, 0) 
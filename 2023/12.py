#!/usr/bin/env python3
import puzzle, functools

def parse_input(INPUT):
  lines = INPUT
  return [(l.split()[0], tuple(map(int, l.split()[1].split(',')))) 
          for l in lines]

def parse_input2(INPUT):
  lines = parse_input(INPUT)
  return [(((a+'?')*5)[:-1], b*5) for a, b in lines]

@functools.cache
def num_possible(raw, instrs):
  if len(instrs) == 0:
    return 0 if '#' in raw else 1
  if raw == '': return 0
  next_instr = instrs[0]
  if raw[0] == '#':
    for i in range(next_instr):
      if i >= len(raw) or raw[i] == '.':
        return 0
    if i + 1 < len(raw) and raw[i+1] == '#': return 0
    return num_possible(raw[next_instr+1:], instrs[1:])
  elif raw[0] == '?':
    # apply next instr OR move forward one
    valid = True
    for i in range(next_instr):
      if i >= len(raw) or raw[i] == '.':
        valid = False
    if i + 1 < len(raw) and raw[i+1] == '#': valid = False
    np1 = num_possible(raw[next_instr+1:], instrs[1:]) if valid else 0
    np2 = num_possible(raw[1:], instrs)
    return np1 + np2
  elif raw[0] == '.':
    return num_possible(raw[1:], instrs)
 
def one(INPUT):
  lines = parse_input(INPUT)
  out = 0
  for raw, instrs in lines:
    np = num_possible(raw, instrs)
    print(raw, instrs, np)
    out += np
  return out

def two(INPUT):
  lines = parse_input2(INPUT)
  print(lines)
  out = 0
  for raw, instrs in lines:
    np = num_possible(raw, instrs)
    print(raw, instrs, np)
    out += np

  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "12")

  p.run(one, 0) 
  p.run(two, 0) 

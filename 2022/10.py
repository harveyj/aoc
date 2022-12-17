#!/usr/bin/env python3
import puzzle

def parse(INPUT):
  ret = []
  for l in INPUT.split('\n'):
    tokens = l.split()
    if len(tokens) == 1:
      ret.append(['noop', 0])
    else:
      ret.append(['noop', 0])
      ret.append(['addx', int(tokens[1])])
  return ret

def one(INPUT):
  X = 1
  pc = 1
  ret = 0
  for instr, rval in parse(INPUT):
    if (pc - 20) % 40 == 0:
      print(X, pc, X*pc)
      ret += X*pc
    if instr == 'addx':
      pc += 1
      X += rval
    else:
      pc += 1
    print('pc', pc,  'X', X)
  return ret

def two(INPUT):
  X = 1
  pc = 1
  ret = 0
  for instr, rval in parse(INPUT):
    loc = (pc-1) % 40
    if X -1 <= loc <= X+1:
      print('#',end='')
    else:
      print('.',end='')
    if pc%40 == 0:
      print('')
    if instr == 'addx':
      pc += 1
      X += rval
    else:
      pc += 1

p = puzzle.Puzzle("10")
# p.run(one, 1)
p.run(two, 1)

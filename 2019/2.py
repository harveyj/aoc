#!/usr/bin/env python3
import puzzle

# you could run this on intputer and maybe i will, but the first version is fun.
def run(a, b, instring):
  ram = list(map(int, instring))

  ram[1] = a
  ram[2] = b

  idx = 0
  while ram[idx] != 99:
    inst = ram[idx]
    if inst == 1:
      ram[ram[idx + 3]] = ram[ram[idx + 1]] + ram[ram[idx+2]]
    elif inst == 2:
      ram[ram[idx + 3]] = ram[ram[idx + 1]] * ram[ram[idx+2]]

    idx += 4
  return ram

def one(INPUT):
  instring = INPUT[0].split(',')
  return run(12, 2, instring)[0]

def two(INPUT):
  instring = INPUT[0].split(',')
  for a in range(1, 100):
    for b in range(1, 100):
      out_val = run(a, b, instring)[0]
      if out_val == 19690720:
        return a*100+b
  return None

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "2")

  p.run(one, 0)
  p.run(two, 0)

#!/usr/bin/env python3
import puzzle, library, math

def parse_input(INPUT):
  return list(map(abs, library.ints(INPUT[0])))

def one(INPUT):
  invals = parse_input(INPUT)
  out = 0
  for i in range(len(invals) // 2):
    a = invals[i*2]; b = invals[i*2+1]
    for val in range(a, b+1):
      split_digits = math.ceil(math.log(val, 10)) // 2
      if val // 10**split_digits == val % 10**split_digits:
        out += val
  return out

def two(INPUT):
  invals = parse_input(INPUT)
  good_vals = set()
  gv_base = {}
  for i in range(len(invals) // 2):
    a = invals[i*2]; b = invals[i*2+1]
    for val in range(a, b+1):
      digits = math.ceil(math.log(val, 10))
      for num_digits in range(1, digits // 2 + 1):
        # leading zeroes can throw you off! ensure that num_digits *exactly* fits
        if digits % num_digits != 0: continue
        tmp_val = val
        base = tmp_val % 10**num_digits
        if base == 0: continue
        dirty = False
        for i in range(0, digits, num_digits):
          if tmp_val % 10**num_digits != base:
            dirty = True
          tmp_val //= 10**num_digits
        if not dirty:
          good_vals.add(val)
          gv_base[val] = base
  return sum(good_vals)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "2")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

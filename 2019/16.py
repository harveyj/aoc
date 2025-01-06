#!/usr/bin/env python3
import puzzle

def one(INPUT):
  def one_round(in_str):
    digits = list(map(int, list(in_str)))
    new_digits = []
    BASE_PAT = [0, 1, 0, -1]
    for i in range(len(digits)):
      pat = []
      for j, num in enumerate(BASE_PAT):
        pat.extend([num] * (i+1))
      # print(pat)
      out = 0
      for j, d in enumerate(digits):
        pat_idx = j+1
        pat_idx %= len(pat)
        out += d * pat[pat_idx]
        # print('%i*%i + ' % (d, pat[pat_idx]), end='')
      out = abs(out)
      out %= 10
      new_digits.append(out)
    ret = ''.join(map(str, new_digits))
    return ret

  out = INPUT[0]
  for i in range(100):
    out = one_round(out)
  return out[:8]

def two(INPUT):
  import math
  INPUT = INPUT[0]
  def one_round(cumsums):
    new_cumsums = [0] * len(cumsums)
    for i in range(len(cumsums)):
      if i > 0:
        new_cumsums[i] = (new_cumsums[i-1] + cumsums[i]) % 10
      elif i == 0:
        new_cumsums[i] = cumsums[i]
    return new_cumsums

  rev_input = list(map(int, INPUT))
  rev_input.reverse()
  idx = int(INPUT[:7])
  dur = len(INPUT)*10000 - idx
  rev_input = rev_input * math.ceil(dur / len(INPUT))
  rev_input = rev_input[:dur]

  digits = rev_input
  for i in range(100):
    digits = one_round(digits)
  answer = digits[-8:]
  answer.reverse()
  return ''.join(map(str, answer))

if __name__ != '__main__':
  p = puzzle.Puzzle("2019", "16")
  p.run(one, 0)
  p.run(two, 0)

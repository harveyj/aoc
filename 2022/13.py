#!/usr/bin/env python3
import puzzle
import functools

def parse(INPUT):
  lines = INPUT.split('\n')
  return [(eval(lines[i]), eval(lines[i+1])) for i in range(0, len(lines), 3)]

def greater(l, r):
  t_l = type(l)
  t_r = type(r)
  # print(t_l, t_r, l, r)
  if t_l is int and t_r is int:
    if l < r:
      return -1
    elif r < l:
      return 1
    else: return 0
  elif t_l is list and t_r is list:
    for i in range(len(l)):
      if len(r) <= i:
        return 1
      val = greater(l[i], r[i])
      if val != 0: return val
    return 0 if len(l) == len(r) else -1
  elif t_l is int:
    return greater([l], r)
  elif t_r is int:
    return greater(l, [r])
  else:
    print("ERROR SHOULD NOT REACH")

# right, right, not, right, not, right, not, not
def one(INPUT):
  pairs = parse(INPUT)
  index = 0
  total = 0
  for l, r in pairs:
    index += 1
    # print(l, r)
    if greater(l, r) == -1:
      total += index
  return total


def parse2(INPUT):
  lines = INPUT.split('\n')
  lines.append('[[2]]')
  lines.append('[[6]]')
  lines.sort()
  lines = [l for l in lines if l]
  return [eval(l) for l in lines]

def two(INPUT):
  pairs = parse2(INPUT)
  pairs = sorted(pairs, key=functools.cmp_to_key(greater))
  t = str([[2]])
  s = str([[6]])

  ans = 1
  for i, p in enumerate(pairs):
    print(p)
    if str(p) in [t, s]:
      print(i+1)
      ans *= (i+1)
  return ans

p = puzzle.Puzzle("13")
# p.run(one, 1)
p.run(two, 1)

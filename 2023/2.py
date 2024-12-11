import puzzle
import re


def one(INPUT):
  out = 0

  def check_valid(l):
    iters = l.split(':')[1].split(';')
    max_r = 12
    max_g = 13
    max_b = 14
    for iter in iters:
      r = re.search('(\d+) red', iter)
      g = re.search('(\d+) green', iter)
      b = re.search('(\d+) blue', iter)
      r = int(r.group(1)) if r else 0
      g = int(g.group(1)) if g else 0
      b = int(b.group(1)) if b else 0
      if r > max_r or g > max_g or b > max_b:
        # print('BAD GAME', l)
        return False
    return True

  for i, l in enumerate(INPUT):
    if check_valid(l):
      out += i + 1
  return out


def two(INPUT):
  out = 0

  def min_items(l):
    iters = l.split(':')[1].split(';')
    max_r = 0
    max_g = 0
    max_b = 0
    for iter in iters:
      r = re.search('(\d+) red', iter)
      g = re.search('(\d+) green', iter)
      b = re.search('(\d+) blue', iter)
      r = int(r.group(1)) if r else 0
      g = int(g.group(1)) if g else 0
      b = int(b.group(1)) if b else 0
      max_r = max(max_r, r)
      max_g = max(max_g, g)
      max_b = max(max_b, b)
    return (max_r, max_g, max_b)

  for i, l in enumerate(INPUT):
    mins = min_items(l)
    out += mins[0] * mins[1] * mins[2]

  return out


if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "2")

  p.run(one, 0) 
  p.run(two, 0) 

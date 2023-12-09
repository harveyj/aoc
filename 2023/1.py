import puzzle
import re

def one(INPUT):
  out = 0
  for l in INPUT.split("\n"):
    s = re.search('(\d)', l)
    e = re.search('(\d)', l[::-1])
    out += int(s.group(0) + e.group(0))
  return out


def two(INPUT):
  re_patterns = [
      '(zero)',
      '(one)',
      '(two)',
      '(three)',
      '(four)',
      '(five)',
      '(six)',
      '(seven)',
      '(eight)',
      '(nine)',
  ]

  def find_first(l):
    min_match = re.search('(\d)', l)
    min_idx = min_match.start() if min_match else 1000000
    min_val = min_match and min_match.group(0)
    print(l, "mi, mv", min_idx, min_val)
    for i, pat in enumerate(re_patterns):
      mat = re.search(pat, l)
      if mat and mat.start() < min_idx:
        min_val = str(i)
        min_idx = mat.start()
    return min_val

  def find_last(l):
    matches = list(re.finditer('(\d)', l))
    match = matches and matches[-1]
    max_idx = match.start() if match else -1
    max_val = match and match.group(0)

    for i, pat in enumerate(re_patterns):
      matches = list(re.finditer(pat, l))
      if matches and matches[-1].start() > max_idx:
        max_val = str(i)
        max_idx = matches[-1].start()
    return max_val

  out = 0
  for l in INPUT.split("\n"):
    s = find_first(l)
    e = find_last(l)
    print('f l', s, e)
    out += int(s + e)
  return out


p = puzzle.Puzzle("1")
p.run(one, 0)
p.run(two, 0)

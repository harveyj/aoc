import puzzle

def one(INPUT):
  ret = 0
  last_val = 1000000000000
  for val in [int(l) for l in INPUT.split('\n')]:
    if val > last_val:
      ret += 1
    last_val = val
  return ret

def two(INPUT):
  processed = [int(l) for l in INPUT.split('\n')]
  window = [processed[i-2] + processed[i-1] + processed[i] for i in range(2, len(processed))]
  total = sum([ 1 if b>a else 0 for a, b in zip(window, window[1:])])
  return total

p = puzzle.Puzzle("1")
p.run(one, 0)
p.run(two, 0)

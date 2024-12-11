import puzzle

def numFishCheap(fish, life, iters):
  total = 0;
  # f(n) = f(n-7) + f(n-9)
  vals = {0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:3, 9:3}
  for i in range(10, iters + 1):
    vals[i] = vals[i - 7] + vals[i - 9];
  return vals[iters]

def puzz(INPUT, iters=256, life=7):
  total = 0
  for i in map(int, '\n'.join(INPUT).split(',')):
    thisFish = numFishCheap([0], life, iters - i);
    total += thisFish;
  return total

def one(INPUT):
  return puzz(INPUT, iters=80)
def two(INPUT):
  return puzz(INPUT, iters=256)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "6")

  p.run(one, 0) 
  p.run(two, 0) 

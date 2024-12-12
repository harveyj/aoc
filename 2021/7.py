import puzzle

def puzz(INPUT, two=False):
  crabs = list(map(int, '\n'.join(INPUT).split(',')))
  crabs.sort()
  median = crabs[len(crabs) // 2];
  deltas = [];
  totalOne = 0;
  for crab in crabs:
    deltas.append(crab - median);
    totalOne += abs(crab - median);

  totalCrabs = sum(crabs)
  mean = round(totalCrabs / len(crabs))
  mean -= 5 # wtf, past Harvey?
  totals = {}
  for i in range(10):
    mean += 1;
    deltas = [];
    total = 0;
    for crab in crabs:
      deltas.append(crab - mean)
      dist = abs(crab - mean)
      total += (dist * (dist + 1)) // 2
    totals[mean] = total;
  totalTwo = min(totals.items(), key=lambda a: a[1])
  return totalTwo[0] if two else totalOne

def one(INPUT):
  return puzz(INPUT)

def two(INPUT):
  return puzz(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "7")

  p.run(one, 0) 
  p.run(two, 0) 

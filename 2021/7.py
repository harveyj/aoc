import puzzle

def puzz(INPUT, two=False):
  crabs = list(map(int, INPUT.split(',')))
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
  return totalTwo if two else totalOne

p = puzzle.Puzzle("7")
p.run(puzz, 0)
p.run(puzz, 0, two=True)

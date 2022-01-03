import puzzle

def process_input(INPUT):
  return [l for l in INPUT.split("\n")]


def one(INPUT):
  processed = process_input(INPUT)
  gamma = ['1' if sum([l[i].count("1")  for l in processed]) > len(processed) / 2 else "0" for i in range(len(processed[0]))]
  epsilon = ['0' if g=='1' else '1' for g in gamma]
  return int(''.join(gamma),2) * int(''.join(epsilon),2);


def two(INPUT):
  pass


p = puzzle.Puzzle("3")
p.run(one, 0)
p.run(two, 0)

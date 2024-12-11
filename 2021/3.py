import puzzle

def process_input(INPUT):
  return [l for l in INPUT]


def one(INPUT):
  processed = process_input(INPUT)
  gamma = ['1' if sum([l[i].count("1")  for l in processed]) > len(processed) / 2 else "0" for i in range(len(processed[0]))]
  epsilon = ['0' if g=='1' else '1' for g in gamma]
  return int(''.join(gamma),2) * int(''.join(epsilon),2);


def two(INPUT):
  processed = process_input(INPUT)
  gamma = ['1' if sum([l[i].count("1")  for l in processed]) > len(processed) / 2 else "0" for i in range(len(processed[0]))]
  most = processed
  for i in range(len(processed[0])):
    b = '1' if sum([l[i].count("1") for l in most]) >= len(most) / 2 else "0"
    most = [a for a in most if a[i] == b]
    if len(most) == 1:
      break
  least = processed
  for i in range(len(processed[0])):
    b = '0' if sum([l[i].count("1") for l in least]) >= len(least) / 2 else "1"
    least = [a for a in least if a[i] == b]
    if len(least) == 1:
      break
  return int(most[0], base=2) * int(least[0], base=2)


if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "3")

  p.run(one, 0) 
  p.run(two, 0) 

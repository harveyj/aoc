import puzzle

def process_input(INPUT):
  return [(l.split()[0], int(l.split()[1])) for l in INPUT.split("\n")]

def one(INPUT):
  instructions = process_input(INPUT)
  depth = 0
  forward = 0
  for (d, mag) in instructions:
    if d == "up":
      depth -= mag
    elif d == "down":
      depth += mag
    elif d == "forward":
       forward += mag;
  return depth * forward

def two(INPUT):
  instructions = process_input(INPUT)
  depth = 0
  aim = 0
  forward = 0
  for (d, mag) in instructions:
    if d == "up":
      aim -= mag
    elif d == "down":
      aim += mag
    elif d == "forward":
       forward += mag;
       depth += aim * mag;
  return depth * forward

p = puzzle.Puzzle("2")
p.run(one, 0)
p.run(two, 0)

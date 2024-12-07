#!/usr/bin/env python3
import puzzle, re, library, itertools

def parse_input(INPUT):
  for l in INPUT:
    yield re.findall('mul\(\d+,\d+\)', l)

def one(INPUT):
  total = 0
  for matches in parse_input(INPUT):
    for match in matches:
      ints = library.ints(match)
      total += ints[0] * ints[1]
  return total

def find_mul(INPUT):
  for match in re.finditer('mul\((\d+),(\d+)\)', INPUT):
    yield (match.start(), 'mul', match.groups())

def find_do(INPUT):
  for match in re.finditer('do\(\)', INPUT):
    yield (match.start(), 'do', match.groups())

def find_dont(INPUT):
  for match in re.finditer('don\'t\(\)', INPUT):
    yield (match.start(), 'dont', match.groups())

def two(INPUT):
  INPUT = ''.join(INPUT)
  muls = find_mul(INPUT)
  dos = find_do(INPUT)
  donts = find_dont(INPUT)
  combined = list(itertools.chain.from_iterable([muls, dos, donts]))
  combined.sort()
  active = True
  out = 0
  for _, action, vals in combined:
    if action == 'do':
      active = True
    elif action == 'dont':
      active = False
    elif action == 'mul' and active:
      out += int(vals[0]) * int(vals[1])
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "3")

  p.run(one, 0)
  p.run(two, 0)

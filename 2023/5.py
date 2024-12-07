#!/usr/bin/env python3
import puzzle
import random
def parse_input(INPUT):
  chunks = INPUT.split('\n\n')
  seeds = list(map(int, chunks[0].split()[1:]))
  def parse_map(raw):
    lines = raw.split('\n')
    header_items = lines[0].split()[0].split('-')
    fr, to = header_items[0], header_items[2]
    ranges = (tuple(map(int, l.split())) for l in lines[1:])
    return fr, to, ranges
  maps = {}
  for c in chunks[1:]:
    fr, to, ranges = parse_map(c)
    maps[fr] = (to, tuple(ranges))
  return seeds, maps

def eval_number(number, start_state, maps, end_state='location'):
  if start_state == end_state: return number
  state = start_state
  while True:
    state, numbers = maps[state]
    for dst, src, size in numbers:
      if src <= number < src + size:
        number = number - src + dst
        break
    if state == end_state:
      return number

def one(INPUT):
  seeds, maps = parse_input(INPUT)
  dests = [eval_number(s, 'seed', maps) for s in seeds]
  return min(dests)

# This is either the proudest or least proud moment of my advent of code career.
def two(INPUT):
  seeds, maps = parse_input(INPUT)
  seed_ranges = [(seeds[n*2], seeds[n*2]+seeds[n*2+1]) for n in range(len(seeds)//2)]
  def rev_items(entry):
    a, b, c = entry
    return b, a, c
  maps_rev = {v[0]: (k, tuple(map(rev_items, v[1]))) for k, v in maps.items()}

  def is_in_interval(idx, layer):
    for (start, end) in layer:
      if start <= idx < end:
        return True
    return False

  hits = []

  for i in range(0, 500000):
    sample = int(random.random() * 100000000)
    if is_in_interval(eval_number(sample, 'location', maps_rev, end_state='seed'), seed_ranges):
      hits.append(sample)
  lowest_found = min(hits)

  for sample in range(lowest_found - 50000, lowest_found):
    if is_in_interval(eval_number(sample, 'location', maps_rev, end_state='seed'), seed_ranges):
      hits.append(sample)

  return min(hits)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "5")

  p.run(one, 0) 
  p.run(two, 0) 
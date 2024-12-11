#!/usr/bin/env python3
import puzzle, re, library, math
from collections import defaultdict

def one(INPUT, n=25):
  array = library.ints(INPUT[0])
  for i in range(n):
    new_array = []
    for stone in array:
      digits = math.ceil(math.log(stone, 10)) if stone not in [1, 0] else 1
      if stone / 10**digits == 1: digits += 1
      if stone == 0:
        new_array.append(1)
      elif digits % 2 == 0:
        new_array.append(round(stone // 10**(digits/2)))
        new_array.append(round(stone % 10**(digits/2)))
      else:
        new_array.append(stone*2024)
      array = new_array
  return len(array)

# TODO replace one with two
def two(INPUT):
  n = 75
  stone_counts = defaultdict(int)
  for val in library.ints(INPUT[0]):
    stone_counts[val] += 1
  for i in range(n):
    new_counts = defaultdict(int)
    for stone_id, stone_count in stone_counts.items():
      digits = math.ceil(math.log(stone_id, 10)) if stone_id not in [1, 0] else 1
      if stone_id / 10**digits == 1: digits += 1
      # print(stone, digits)
      if stone_id == 0:
        new_counts[1] += stone_count
      elif digits % 2 == 0:
        new_counts[round(stone_id // 10**(digits/2))] += stone_count
        new_counts[round(stone_id % 10**(digits/2))] += stone_count
      else:
        new_counts[stone_id*2024] += stone_count
      stone_counts = new_counts
  return sum(stone_counts.values())

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "11")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

#!/usr/bin/env python3
import puzzle
import math

def parse(INPUT):
  return int(INPUT)

def factorization(n):
  factors = []
  for i in range(1, math.ceil(n/2) + 1):
    if n // i == n / i:
      factors.append(i)
  return factors + [n]

def bin2num(indices):
  tot = 0
  for i in range(len(indices)):
    tot += indices[i] * 2**i
  return tot


def one(INPUT):
  max = parse(INPUT) / 10
  for i in range(100):
    prev = sum(factorization(2**(i-1)))
    cur = sum(factorization(2**i))
    if prev < max < cur:
      print(i)
      break
  indices = [0] * 21
  indices[20] = 1
  indices[19] = 0
  indices[18] = 0
  indices[17] = 0
  indices[16] = 1
  indices[15] = 0
  indices[14] = 0
  indices[13] = 0
  indices[12] = 0
  indices[11] = 0 ##
  indices[10] = 0
  indices[9] = 1
  indices[8] = 0

  for j in range(i):
    prev = sum(factorization(bin2num(indices)))
    print(bin2num(indices))
    indices[8] = 1
    print(bin2num(indices))
    cur = sum(factorization(bin2num(indices)))
    if prev < max < cur:
      print("yes", indices)
      break
  print(bin2num(indices))
  for i in range(665280, 600000, -10): # 693000
    if sum(factorization(i)) > max:
      print("found", i)
  # # print(factorization(6))
  # last_seen = 0; i = 3
  # while last_seen < max:
  #   last_seen = sum(factorization(i))
  #   if max / last_seen > 2:
  #     i *= max / last_seen
  #   else: i += 1
  #   print(i, sum(factorization(i)))
  # return 0

def two(INPUT):
  # 715000
  for i in range(700000, 705600+1, 1):
    factors = factorization(i)
    filtered = [f for f in factors if i / f <= 50]
    tot = sum([f * 11 for f in filtered])
    if tot >= 29000000:
      print(i, tot)
  return 0

p = puzzle.Puzzle("20")
# p.run(one, 0)
p.run(two, 0)

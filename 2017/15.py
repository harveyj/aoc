#!/usr/bin/env python3
import puzzle, library
import re

def parse(INPUT):
  return list(map(int, INPUT[0].split(',')))

def one(INPUT):
  a, b = parse(INPUT)
  a_mul = 16807; b_mul = 48271
  mod_fact = 2147483647
  rounds = 40000000
  count = 0
  for i in range(rounds):
    a = (a * a_mul) % mod_fact
    b = (b * b_mul) % mod_fact
    # print(a, b)
    if bin(a)[-16:] == bin(b)[-16:]:
      count += 1
  return count

def all_a(a):
  a_mul = 16807
  mod_fact = 2147483647
  while True:
    a = (a * a_mul) % mod_fact
    if a % 4 == 0:
      yield a

def all_b(b):
  b_mul = 48271
  mod_fact = 2147483647
  while True:
    b = (b * b_mul) % mod_fact
    if b % 8 == 0:
      yield b

def two(INPUT):
  a, b = parse(INPUT)
  a_s = all_a(a)
  b_s = all_b(b)
  rounds = 5000000
  # rounds = 5
  count = 0
  for a, b in zip(a_s, b_s):
    rounds -= 1
    # print(a, b)
    if bin(a)[-16:] == bin(b)[-16:]:
      count += 1
      print(5000000-rounds)
    if rounds == 0:
      return count

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "15")

  p.run(one, 0) 
  p.run(two, 0) 

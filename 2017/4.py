#!/usr/bin/env python3
import puzzle

def parse2(INPUT):
  for l in INPUT:
    yield [''.join(sorted(word)) for word in l.split()]


def parse(INPUT):
  for l in INPUT:
    yield l.split()


def two(INPUT):
  total = 0
  for l in parse2(INPUT):
    if len(set(l)) == len(l):
      total += 1
  return total

def one(INPUT):
  total = 0
  for l in parse(INPUT):
    if len(set(l)) == len(l):
      total += 1
  return total

p = puzzle.Puzzle("2017", "4")
p.run(one, 0)
p.run(two, 0)

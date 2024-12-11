#!/usr/bin/env python3
import puzzle
import re

def parse_line(l):
  pat = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
  a, b, c, d = [int(i) for i in re.match(string=l, pattern=pat).groups()]
  return [a, b, c, d]

def one(INPUT):
  processed_input = [parse_line(l) for l in INPUT]
  out = []
  for a, b, c, d in processed_input:
    if a <= c and b >= d or a >= c and b <= d:
      out.append([a, b, c, d])
  print(processed_input)
  print(out)
  return len(out)

def two(INPUT):
  processed_input = [parse_line(l) for l in INPUT]
  out = []
  for a, b, c, d in processed_input:
    if a <= c <= b or a <= d <= b or a <= c and b >= d or a >= c and b <= d:
      out.append([a, b, c, d])
  print(processed_input)
  print(out)
  return len(out)

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "4")

  p.run(one, 0) 
  p.run(two, 0) 

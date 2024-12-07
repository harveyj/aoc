#!/usr/bin/env python3
import puzzle
import re
import math

def parse_input(INPUT):
  instrs, network = INPUT.split('\n\n')
  network_map = dict()
  for l in network.split('\n'):
    print(l)
    mat = re.match("(\w+) = \((\w+), (\w+)\)", l)
    key, left, right = mat.group(1,2,3)
    network_map[key] = {'L': left, 'R': right}
  return instrs, network_map

def one(INPUT):
  instrs, network_map = parse_input(INPUT)
  node = 'AAA'
  out = 0
  while True:
    for i in instrs:
      out += 1
      node = network_map[node][i]
    if node == 'ZZZ':
      return out

def two(INPUT):
  def score(start, instrs, network_map):
    steps = 0
    node = start
    while True:
      for i in instrs:
        steps += 1
        node = network_map[node][i]
        print(len([k for k in nodes if k[-1] == 'Z']), end='')
        if node[-1] == 'Z':
          return steps

  instrs, network_map = parse_input(INPUT)
  nodes = [k for k in network_map if k[-1] == 'A']
  outs = dict()
  for start in nodes:
    outs[start] = score(start, instrs, network_map)
  return math.lcm(*[outs[k] for k in outs])

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "8")

  p.run(one, 0) 
  p.run(two, 0) 

#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  return '\n'.join(INPUT).split(',')

def hash(instr):
  cv = 0
  for c in instr:
    cv = ((cv + ord(c)) * 17) % 256
  return cv

def one(INPUT):
  invals = parse_input(INPUT)
  outs = [hash(iv) for iv in invals]
  return sum(outs)

def sum_box(box):
  return sum([(i+1) * entry[1] for i, entry in enumerate(box)])

def two(INPUT):
  invals = parse_input(INPUT)
  boxes = [[] for i in range(256)]
  for iv in invals:
    if '-' in iv:
      label = iv[:-1]
      box = hash(label)
      for i, lens in enumerate(boxes[box]):
        if label == lens[0]:
          del boxes[box][i]
    else:
      label, power = iv.split('=')
      box = hash(label)
      if power != str(int(power)):
        print('ERROR', power)
      power = int(power)
      replace = False
      for i, lens in enumerate(boxes[box]):
        if label == lens[0]:
          lens[1] = power
          replace = True
      if not replace:
        boxes[box].append([label, power])
    # print(iv, [(i, boxes[i]) for i in range(255) if len(boxes[i]) > 0])
  fps = [(i+1) * sum_box(boxes[i]) for i in range(256) if len(boxes[i]) > 0]
  return sum(fps)


if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "15")

  p.run(one, 0) 
  p.run(two, 0) 

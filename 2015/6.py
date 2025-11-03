#!/usr/bin/env python3
import puzzle
import re
from library import Grid
from collections import defaultdict

def parse(INPUT):
  instrs = []
  for l in INPUT:
    if 'toggle' in l:
      instr = ['toggle']
    elif 'turn on' in l:
      instr = ['turn on']
    else:
      instr = ['turn off']
    match = re.findall(r'(\d+)', l)

    for m in match:
      instr.append(int(m))
    instrs.append(instr)
  return instrs

# spatial index of instructions, scan l-r 
def one(INPUT):
  rows = defaultdict(list)
  instrs = parse(INPUT)
  for inst in instrs:
    (op, x1, y1, x2, y2) = inst
    for y in range(y1, y2+1):
      row_ops = rows[y]
      row_ops.append((op, x1, x2))
  on_lights = 0
  for y in range(1000):
    ops = rows[y]
    for x in range(1000):
      on = 0
      for op in ops:
        oper, x1, x2 = op
        if x1 <= x <= x2:
          if oper == "turn on":
            on = 1
          if oper == "turn off":
            on = 0
          if oper == "toggle":
            on = 0 if on == 1 else 1
      on_lights += on
  print(on_lights)
  return on_lights

def two(INPUT):
  rows = defaultdict(list)
  instrs = parse(INPUT)
  for inst in instrs:
    (op, x1, y1, x2, y2) = inst
    for y in range(y1, y2+1):
      row_ops = rows[y]
      row_ops.append((op, x1, x2))
  on_lights = 0
  for y in range(1000):
    ops = rows[y]
    for x in range(1000):
      on = 0
      for op in ops:
        oper, x1, x2 = op
        if x1 <= x <= x2:
          if oper == "turn on":
            on += 1
          if oper == "turn off":
            on = max(on - 1, 0)
          if oper == "toggle":
            on += 2
      on_lights += on
  print(on_lights)
  return on_lights

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "6")

  p.run(one, 0)
  p.run(two, 0)

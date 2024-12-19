#!/usr/bin/env python3
import puzzle
import intputer

def onetwo(INPUT, two=False):
  instructions = list(map(int, INPUT[0].split(',')))
  puters = [intputer.Intputer(instructions, inputs=[i], id=i) for i in range(50)]
  nat_x, nat_y = None, None
  all_idle_start = -1
  values = set()
  for i in range(1000000):
    for p in puters:
      # ensure that the input queue is either [-1] or the output that it should be 
      if p.inputs == []:
        p.inputs.append(-1)
      p.step()
      if len(p.outputs) == 3:
        dest, x, y = p.outputs
        if dest == 255:
          if not two:
            return y
          nat_x, nat_y = x, y
          p.outputs = []
        else:
          if puters[dest].inputs == [-1]:
            puters[dest].inputs = []
          puters[dest].inputs += [x, y]
          # print(f'OUT: {dest, x, y}, in: {puters[dest].inputs}')
          p.outputs = []
    if two:
      all_idle = len([p.inputs for p in puters if p.last_read == -1]) == 50
      if all_idle:
        if all_idle_start == -1:
          all_idle_start = i
        if i - all_idle_start > 100:
          puters[0].inputs = [nat_x, nat_y]
          for p in puters: p.last_read = None
          # print(f'REBOOT: {nat_x, nat_y}')
          all_idle_start = -1
          # print(values)
          if nat_y in values:
            return nat_y
          else: values.add(nat_y)
      else: all_idle_start = -1

def one(INPUT):
  return onetwo(INPUT, two=False)

def two(INPUT):
  return onetwo(INPUT, two=True)

p = puzzle.Puzzle("2019", "23")
# p.run(one, 0)
p.run(two, 0)

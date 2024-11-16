#! /usr/bin/env python3

import intputer

class SpringDroid(object):

  def __init__(self, code, instructions):
    inputs = list(map(ord, code))
    self.puter = intputer.Intputer(instructions, inputs, id='a')
    self.outputs = []

  def run(self):
    for i in range(10000):
      code, out = self.puter.run()
      if code == intputer.Intputer.OUTPUT:
        print("OUTPUT", out)
        self.outputs.append(out)
      elif code == intputer.Intputer.INPUT: 
        next_ip = raw_input()
        print("INPUT", next_ip)
        break
      else:
        # print("foo")
        break
    return self.outputs

  def run2(self):
    self.puter.run2()
    return self.puter.outputs


# J = A or B or C and NOT D
def one(INPUT):
  prog = """
  NOT A T
  OR T J
  NOT B T
  OR T J
  NOT C T
  OR T J
  AND D J
  WALK
"""
  instructions = INPUT[0].split(',')
  prog = prog[1:]
  sd = SpringDroid(prog, instructions)

  out = sd.run2()
  for c in out:
    if c > 255:
      print(c)
    else: 
      print(chr(c), end='')


def two(INPUT):
  prog = """
  OR A J
  AND B J
  AND C J
  NOT J J
  OR E T
  OR H T
  AND T J
  AND D J
  NOT A T
  OR T J
  RUN
  """

  instructions = INPUT[0].split(',')
  prog = prog[1:]
  sd = SpringDroid(prog, instructions)

  out = sd.run2()
  for c in out:
    if c > 255:
      print(c)
    else: 
      print(chr(c), end='')

import puzzle 

p = puzzle.Puzzle("2019", "21")
p.run(one, 0)
# p.run(two, 0)

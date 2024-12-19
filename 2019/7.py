#!/usr/bin/env python3
import puzzle
from intputer import Intputer

import itertools

def one(INPUT):
  instructions = list(map(int, INPUT[0].split(',')))

  def chained_amplify(seq, n, a_in):
    puters = []
    for i in range(n): puters.append(Intputer(instructions, id=i))
    outputs = [a_in]
    for i, puter in enumerate(puters):
      puter.inputs = [seq[i], outputs[i]]
      puter.run()
      outputs.append(puter.outputs[-1])
    return outputs[-1]
  outs = [chained_amplify(seq, 5, 0)  for seq in itertools.permutations(range(5))]
  return max(outs)

def two(INPUT):
  instructions = list(map(int, INPUT[0].split(',')))
  def looped_amplify(seq, n, a_in):
    puters = []
    for i in range(n): puters.append(Intputer(instructions, id=i, input_mode='user', output_mode='halt'))
    for i, puter in enumerate(puters): puter.inputs = [seq[i]]
    outputs = [a_in]
    for i in range(10000):
      for ip in puters:
        ip.halted = False
        ip.inputs.append(outputs[-1])
        ip.run()
        outputs.append(ip.outputs[-1])
      if len([ip for ip in puters if ip.terminated]) == 5:
        return outputs[-1]
    print('ERROR')
  # looped_amplify([9,8,7,6,5], n=5, a_in=0)
  outs = [looped_amplify(seq, n=5, a_in=0)  for seq in itertools.permutations(range(5, 10))]
  return max(outs)

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "7")

  p.run(one, 0)
  p.run(two, 0)

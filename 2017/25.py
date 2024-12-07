#!/usr/bin/env python3
import puzzle, library
import re
from collections import defaultdict


def parse_chunk(chunk):
  lines = chunk.split('\n')
  # print(lines)
  state = lines[0].split()[-1][0]
  zero_out = int(lines[2].split()[-1][0])
  zero_slot = lines[3].split()[-1][:-1]
  zero_state = lines[4].split()[-1][0]
  one_out = int(lines[6].split()[-1][0])
  one_slot = lines[7].split()[-1][:-1]
  one_state = lines[8].split()[-1][0]
  return state, (zero_out, zero_slot, zero_state), (one_out, one_slot, one_state)


def one(INPUT):
  state = INPUT[0].split()[-1][0]
  steps = int(INPUT[1].split()[-2])
  tape = defaultdict(int)
  tape_idx = 0

  raw = '\n'.join(INPUT[2:]).strip()
  chunks = map(parse_chunk, raw.split('\n\n'))
  chunks_dict = {state: (zero, one) for state, zero, one in chunks}
  for i in range(0, steps):
    zero, one = chunks_dict[state]
    out, slot, state = (zero if tape[tape_idx] == 0 else one)
    tape[tape_idx] = out
    tape_idx += (1 if slot == 'right' else -1)
    # print(out, slot, state)
  return list(tape.values()).count(1)

def two(INPUT):
  print('Merry Christmas!')
  return 20171225

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "25")

  p.run(one, 0) 
  p.run(two, 0) 
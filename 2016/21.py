#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib
import copy, itertools


def parse(INPUT):
  pat_swap_pos = re.compile('swap position (\d+) with position (\d+)')
  pat_swap_let = re.compile('swap letter (\w+) with letter (\w+)')
  pat_rot_n = re.compile('rotate (\w+) (\d+) \w+') # step/steps don't care
  pat_rot_letter = re.compile('rotate based on position of letter (\w+)')
  pat_reverse = re.compile('reverse positions (\d+) through (\d+)')
  pat_move = re.compile('move position (\d+) to position (\d+)')
  for l in INPUT:
    match_swap_pos = re.match(pat_swap_pos, l)
    match_swap_let = re.match(pat_swap_let, l)
    match_rot_n = re.match(pat_rot_n, l)
    match_rot_letter =re.match(pat_rot_letter, l)
    match_reverse = re.match(pat_reverse, l)
    match_move = re.match(pat_move, l)
    if match_swap_pos: 
      yield ('swap_pos', int(match_swap_pos.group(1)), int(match_swap_pos.group(2)))
    elif match_swap_let:
      yield ('swap_let', match_swap_let.group(1), match_swap_let.group(2))
    elif match_rot_n:
      yield ('rot_n', match_rot_n.group(1), int(match_rot_n.group(2)))
    elif match_rot_letter:
      yield ('rot_letter', match_rot_letter.group(1))
    elif match_reverse:
      yield ('reverse', int(match_reverse.group(1)), int(match_reverse.group(2)))
    elif match_move:
      yield ('move', int(match_move.group(1)), int(match_move.group(2)))
    else:
      yield None

# swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
# swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
# rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
# rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
# reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
# move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.

def transform(inst, inval):
  outval = copy.copy(inval)
  if inst[0] == 'swap_pos':
    outval[inst[2]] = inval[inst[1]]
    outval[inst[1]] = inval[inst[2]]
  elif inst[0] == 'swap_let':
    swap = {inst[1]: inst[2], inst[2]: inst[1]}
    outval = [swap[c] if c in swap else c for c in inval]
  elif inst[0] == 'rot_n':
    rot = inst[2]
    if inst[1] == 'left':
      # [0, 1, 2, 3] -> [1, 2, 3, 0]
      outval = inval[rot:] + inval[:rot]
    else:
      # [0, 1, 2, 3] -> [3, 1, 2]
      outval = inval[-rot:] + inval[:-rot]
  elif inst[0] == 'rot_letter':
    idx = inval.index(inst[1])
    rot = idx + 1 + (1 if idx >= 4 else 0)
    rot %= len(outval)
    outval = inval[-rot:] + inval[:-rot]
  elif inst[0] == 'reverse':
    a, b = inst[1], inst[2]
    for i in range(b-a+1):
      outval[a+i] = inval[b-i]
  elif inst[0] == 'move':
    c =  outval[inst[1]]
    del outval[inst[1]]
    outval.insert(inst[2], c)
  return outval

def encode(INPUT, val):
  for inst in parse(INPUT):
    val = transform(inst, val)
  return val

def one(INPUT):
  val = list('abcdefgh')
  return encode(INPUT, val)

def two(INPUT):
  for combo in itertools.permutations(list('abcdefgh'), 8):
    # print(combo)
    if encode(INPUT, combo) == list('fbgdceah'):
      return ''.join(combo)

p = puzzle.Puzzle("21")
# p.run(one, 0)
p.run(two, 0)

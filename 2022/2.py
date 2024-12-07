#!/usr/bin/env python3
import puzzle

def points_win(a, b):
  if a == 'A':
    if b == 'X': return 3
    elif b == 'Y': return 6
    elif b == 'Z': return 0
  elif a == 'B':
    if b == 'X': return 0
    elif b == 'Y': return 3
    elif b == 'Z': return 6
  elif a == 'C':
    if b == 'X': return 6
    elif b == 'Y': return 0
    elif b == 'Z': return 3
        
def points_shape(b):
  if b == 'X': return 1
  elif b == 'Y': return 2
  elif b == 'Z': return 3

# What beats the input val
def beats_rps(a):
  if a == 'A':
    return 'Y'
  elif a == 'B':
    return 'Z'
  elif a == 'C':
    return 'X'

def draws_rps(a):
  if a == 'A':
    return 'X'
  elif a == 'B':
    return 'Y'
  elif a == 'C':
    return 'Z'

# What loses to the input value
def loses_rps(a):
  if a == 'A':
    return 'Z'
  elif a == 'B':
    return 'X'
  elif a == 'C':
    return 'Y'


def one(INPUT):
  processed_input = [val.split(" ") for val in INPUT]

  total = 0
  for a, b in processed_input:
    total += points_win(a, b) + points_shape(b)
  ANSWER_1 = total
  return ANSWER_1

def two(INPUT):
  final_input=[]

  processed_input = [val.split(" ") for val in INPUT]
  # X means p1 need to win, Y means you need to end the round in a draw, and Z means p1 needs to lose. Good luck!"
  for a, b in processed_input:
    if b == 'X':
      new_b = loses_rps(a)
    elif b == 'Y':
      new_b = draws_rps(a)
    elif b == 'Z':
      new_b = beats_rps(a)
    final_input.append([a, new_b])

  total = 0
  for a, b in final_input:
    total += points_win(a, b) + points_shape(b)
  ANSWER_2 = total
  return ANSWER_2


if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "2")

  p.run(one, 0) 
  p.run(two, 0) 

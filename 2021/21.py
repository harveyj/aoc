#!/usr/bin/env python3
import puzzle
from library import ints
from collections import defaultdict
import itertools

def rotate(n, m):
  return (n-1) % m + 1

def one(INPUT):
  def roll(start):
    return (start, start + 1 % 100, start + 2 % 100)
  pos1, pos2 = ints(INPUT[0])[1], ints(INPUT[1])[1]
  # key = (dice val, pos1, pos2) (player 1 rolls next), val = score1, score2
  outcomes = defaultdict(list) 
  die = 1
  score1, score2 = 0, 0
  for i in range(1000):
    pos1 = rotate(pos1 + sum(roll(die)), 10)
    die = rotate((die + 3), 100)
    pos2 = rotate(pos2 + sum(roll(die)), 10)
    die = rotate((die + 3), 100)
    score1 += pos1
    if score1 >= 1000:
      # oy. dice are rolled 6 times a turn. +1 for zero-indexing. -3 because half turn.
      return score2 * ((i+1)*6-3)
    score2 += pos2
    if score2 >= 1000:
      return score1 * ((i+1)*6)
    outcomes[die, pos1, pos2].append((score1, score2))

# the three rolls of the quantum die is actually just one big roll, all that matters is the probability distro of the sum of the three rolls
# dynamic programming?
# game state can be modeled by:
# a_pos, a_left, a_rolls, b_pos, b_left, b_rolls
# start state is 4, 21, 3, 6, 21, 'a', 0
# f(state) --> # times a wins, # times b wins
# f(state) --> [outcomes] dot product f(state+outcome)

def two(INPUT):
  def counts(lst):
    return {a: lst.count(a) for a in set(lst)}

  pos1, pos2 = ints(INPUT[0])[1], ints(INPUT[1])[1]  
  roll_outcomes = [a+b+c for a,b,c in list(itertools.product([ 1, 2, 3], repeat=3))]

  def rotate(n):
    return (n-1) % 10 +1

  # key -> game state
  # val -> (a wins, b wins)
  outcomes = {}

  def new_outcomes(outcomes, a_pos, a_left, b_pos, b_left, turn):
    a_wins = 0
    b_wins = 0
    if turn == 'a':
      for roll in roll_outcomes:
        new_a_pos = rotate(a_pos+roll)
        new_a_left = a_left - new_a_pos
        turn = 'b'
        if new_a_pos >= a_left:
          a_wins += 1
        else:
          hyp_a_wins, hyp_b_wins = outcomes[(new_a_pos, new_a_left, b_pos, b_left, turn)]
          a_wins += hyp_a_wins
          b_wins += hyp_b_wins
    else:
      for roll in roll_outcomes:
        new_b_pos = rotate(b_pos+roll)
        new_b_left = b_left - new_b_pos
        turn = 'a'
        if new_b_pos >= b_left:
          b_wins += 1
        else:
          hyp_a_wins, hyp_b_wins = outcomes[(a_pos, a_left, new_b_pos, new_b_left, turn)]
          a_wins += hyp_a_wins
          b_wins += hyp_b_wins
    return a_wins, b_wins


  for a_left in range(1, 22):
    for b_left in range(1, 22):
      for a_pos in range(1, 11):
        for b_pos in range(1, 11):
          outcomes[(a_pos, a_left, b_pos, b_left, 'a')] = new_outcomes(outcomes, a_pos, a_left, b_pos, b_left, 'a')
          outcomes[(a_pos, a_left, b_pos, b_left, 'b')] = new_outcomes(outcomes, a_pos, a_left, b_pos, b_left, 'b')

  a, b = outcomes[(pos1, 21, pos2, 21, 'a')]
  return max(a, b)

p = puzzle.Puzzle("2021", "21")
print(p.run(one, 0))
print(p.run(two, 0))
import itertools

INPUT_TEST = (4, 8)
INPUT_FULL = (9, 6)

loc1, loc2 = INPUT_FULL

def counts(lst):
  return {a: lst.count(a) for a in set(lst)}

roll_outcomes = [a+b+c for a,b,c in list(itertools.product([ 1, 2, 3], repeat=3))]

# the three rolls of the quantum die is actually just one big roll, all that matters is the probability distro of the sum of the three rolls
# dynamic programming?
# game state can be modeled by:
# a_pos, a_left, a_rolls, b_pos, b_left, b_rolls
# start state is 4, 21, 3, 6, 21, 'a', 0
# f(state) --> # times a wins, # times b wins
# f(state) --> [outcomes] dot product f(state+outcome)

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
INPUT_TEST = (4, 8)
INPUT_FULL = (9, 6)

a, b = outcomes[(9, 21, 6, 21, 'a')]
print(max(a, b))

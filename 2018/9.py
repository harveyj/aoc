#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict, deque

# two is too slow, by design
def one_slow(INPUT, two=False):
  players, end_marble = library.ints(INPUT[0])
  if two: end_marble *= 100
  marble_id = 4
  current_idx = 3
  marbles = [0,2,1,3] # skip first few steps
  scores = defaultdict(int)
  while marble_id < end_marble+1:
    if marble_id % 1000 == 0:
      print(marble_id)
    if marble_id % 23 == 0:
      seven_back_idx = (current_idx + len(marbles) - 7 ) % len(marbles)
      scores[marble_id % players] += marble_id + marbles[seven_back_idx]
      del marbles[seven_back_idx]
      current_idx = seven_back_idx
    else:
      current_idx = (current_idx + 2) % len(marbles)
      marbles.insert(current_idx, marble_id)
    marble_id += 1
  # print(' '.join([str(m).zfill(2) for m in marbles]))
  return max(scores.values())

def one(INPUT, two=False):
  players, end_marble = library.ints(INPUT[0])
  if two: end_marble *= 100
  marble_id = 4
  marbles = deque([0,2,1,3]) # skip first few steps
  marbles.rotate(-3)
  scores = defaultdict(int)
  # current index always at zero
  while marble_id < end_marble+1:
    if marble_id % 23 == 0:
      scores[marble_id % players] += marble_id
      marbles.rotate(7)
      scores[marble_id % players] += marbles.popleft()
    else:
      marbles.rotate(-2)
      marbles.appendleft(marble_id)
    marble_id += 1
  return max(scores.values())

def two(INPUT):
  return one(INPUT, two=True)

# 2:47 +1min - 3:09 (pt 1) --> 3:35 (pt 2)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "9")
  print(p.run(one, 1))
  print(p.run(two, 0))
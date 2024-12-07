#!/usr/bin/env python3
import puzzle

def one(INPUT):
  processed_input = [[int(sub_val) for sub_val in val.split("\n")] for val in INPUT.split("\n\n")]
  summed_input = [sum(vals) for vals in processed_input]
  return max(summed_input)
  
def two(INPUT):
  processed_input = [[int(sub_val) for sub_val in val.split("\n")] for val in INPUT.split("\n\n")]
  summed_input = [sum(vals) for vals in processed_input]

  summed_input.sort()
  return sum(summed_input[-3:])

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "1")

  p.run(one, 0) 
  p.run(two, 0) 

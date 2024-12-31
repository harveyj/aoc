# Advent of Code 2018
## Overview
My first AOC year but the code is lost to the sands of time.

Redo started November 2024

## Day 1
Warmup! Done in 5 minutes

Difficulty: 1/10

## Day 2
Warmup! Done in 5 minutes

Difficulty: 2/10

## Day 3
Bumping up a little bit - 10 minutes

Difficulty: 3/10

## Day 7
Custom topological sort! Now we're getting into it. 

REWRITE: 12/15/24

Difficulty: 5/10

## Day 8
Recursive tree parse / traversal. Fun one.

REWRITE: 12/30/24 from Thomas's nursery. One month!

Difficulty: 5/10

## Day 9 
Interval math! Edit: OK, not interval math, "do you know how to use a linked list".

Part 1 done in 20 minutes, just a few fiddly edge cases. 
Part 2 done in 20 minutes, use a deque!

REWRITE 12/30/24

Difficulty: 4/10

Lessons learned: Python lists are more like arrays, not like linked lists. Inserts and dels require full copies. Deque is much preferred for applications like many in AOC where you have lots of inserts/deletes at one spot.

## Day 11
Search for largest region over a crypto-y grid.

Part 1: Straightforward impl of puzzle as described.
Part 2: Realize that calculation can be done in O(1) time with an O(N^2) precomputation step. Initial impl was O(N^4)+.

Lesson learned: DEBUG USING SIMPLE EXAMPLES, build up from base components that are trusted!

## Day 12
Detect the period. Added a detect_steady_state function to the library to do this in an automated fashion in the future.

Difficulty: 4.5/10

## Day 13
Simulate mine carts! Fun but READ THE PROBLEM, HARVEY

Rewrite 12/31/2024

Difficulty: 5/10

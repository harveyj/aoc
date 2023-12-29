# Advent of Code 2021
## Overview
Another pure Python year. This year with Capen!

Started 12/1/2021, finished 12/28/2023. I took 12/23- 12/26 almost entirely off. 

## Day 1
Warmup

Difficulty: 2/10

## Day 2
Warmup

Difficulty: 2/10

## Day 3
Gears - mostly a warmup.

Difficulty: 3/10

## Day 4
Giant tree expansion.

Difficulty: 5/10
## Day 5
A big tree walk.

Part 2 I did monte carlo style, sampling to find the rough lowest item and then sequentially checking each number below to ensure there was no hidden lower range.

Difficulty: 6/10

## Day 6
Boat start simulation.

I wish the twist was "you can depress the button whenever you want" - that would force some real 6.046 action.

Difficulty: 5/10

## Day 7
Card game / poker with alternate rules. 

## Day 8
LCM and find the cycle makes its appearance!

Difficulty: 5/10

Location: CT

## Day 9
Tree of difference sums. Super fun, a bit easy (but par for day 9) - a nice romp. 

Difficulty: 5/10

Location: CT

## Day 10
Pipe maze, what is in the pipe loop. A great mix of coding and thinking through. 

Difficulty: 6.5/10

Location: CT

## Day 11
"cosmic expansion" - list comprehensions and math made this one quick. Quite enjoyable.

Difficulty: 6/10

Location: CT

## Day 12
Fill in the regex-ish thing in all possible ways. Again, the perfect level of challenge. I freaking love memoization and functools is fantastic at it. 

Difficulty: 6.5/10

Location: CT

## Day 13
Really hitting my stride. Find the mirrored patterns. Part 1 and part 2 were very list comprehension-able.

Difficulty: 5/10

Location: CT

## Day 14
Rocks sliding around like a tabletop game. 

Part 1 a nice sim.
Part 2 a canonical "find the cycle" AOC puzzle.

Difficulty: 6.5/10

Location: CT

## Day 15
Part 1 a nice amuse

Part 2 took 3 hours longer, pulled a reddit solution, all to find i had a 255 rather than a 256 somewhere...

Difficulty 6/10 but 8/10 because I am dumb.

Location: CT

## Day 16
Energy beams!

A fun one. 

Difficulty: 6/10

Location: CT

## Day 17
Traverse the crucibles losing minimal heat. 

Expressable in a multi-layer graph and then djikstra-able. I love it. Probably my favorite puzzle of AOC this year.

Difficulty: 6/10

Location: CT

## Day 18
Giant-ass lagoon.

Just for the fun of it, I expressed part one in a way that the code for day 10 could solve for me. Part 2 absolutely murdered me with off by one errors. My segment map was correct-ish in terms of being time/space efficient, but corner cases abounded. The fact that the lagoon was n=1 wide rather than n=0 wide was the cause of many of them

harveyj
  ok FINALLY
  i have the main test case passing for part 2
  IT'S OVER MR FRODO
  https://open.spotify.com/track/2SolqzPfBxKpURJbjTV5EJ?si=e73c6cf97b024726

Difficulty: 8.5/10

## Day 19
XMAS network! I loved this puzzle. Right amount of challenge. having XMAS be a variable/constant name is a delight. 

Difficulty: 7.5/10

## Day 20
Flip flop and conjunction network. This one was a beast. My mistake was that I only looked at the *end* of each propagation, not looking to a low pulse being sent at *any* time. Once I got that, things fell into place quickly. I did derive "manually inspect the graph network" on my own, which was the other key insight.

Difficulty: 9.5/10

Location: CT

## Day 21
Traverse the infinite maze. The peak of this year's AOC.
Part 1 is a nice warmup and I reimplemented it time after time to try to nail down part 2. 
Part 2 was brutal for me, I ended up reading several implementations, understanding them, and then implementing my own version. My notebooks had some of the right ideas (the periodicity of the expansion) but I was far away from solving the quadtratic. 

Difficulty: 10/10

Where: Train to NYC for xmas eve, many other places

## Day 22
Tetris-ish with falling blocks. 

Part 2: ~direct reuse of part 1

Solution notes: I struggled with the implementation of part 2 for a while. My first approach kept all blocks logically together in a sorted array. Most approaches I could think of to do this were O(N^4). Eventually I did an approach which had an extra O(N^3) term because the size of (x, y, z) mattered. 

Difficulty: 7/10

Where: Cab back on xmas eve, CT

## Day 23

Longest path through a maze. Longest path problems are in general NP-complete?? Not clear what the solution was "supposed" to be here.
Part 1: Create a graph, do all simple paths
Part 2: Same approach fails to terminate in reasonable time, rewrite the graph to collapse redundant nodes.

Location: Airplane/Airplane 

Topics:
* Graph paths, dfs/bfs

Difficulty: 7/10

## Day 24
Find the intersections of the meteor shower. Part 1 was a quick enjoyable romp through algebra. Part 2 was the last part of AOC for this year, and I had to refresh myself on a bunch of algebra. After a few failed tries at just coding it up, I expressed the puzzle as a series of parametric equations. I then massaged the equations down to n=6 via variable elimination. From there, I plugged them into scipy's equation solver. I had to perform percussive maintenance and try hundreds of times in a loop before I got a plausible solution for the full output. Went out to dinner and was ready to give up, came back from dinner and the solution presented itself in five minutes. 

Location: Airplane / San Juan

Topics
* Basic Algebra through to linear algebra and systems of equations
* Parametric equations

Difficulty: 8/10

## Day 25
Sever a graph network by cutting only three wires. I poked around on networkx documentation until I found a function that did exactly what I wanted. Part 2 was the traditional victory lap. I did this second to last in practice (24-2 was the last puzzle for real).

Location: San Juan/San Juan

Topics
* Graph theory, especially cut theory

Difficulty: 5/10
# Advent of Code 2024
## Overview
Another pure Python year. Capen year 2!

Started 12/2/2024, finished ??.

## Day 1
Pure Warmup. Done from Stamford Hospital with Thomas <3

Difficulty: 1/10

# Day 2
Done from Stamford Hospital. Kinda fiddly for day 2!

Difficulty: 3/10

# Day 3
Regex + state machine. Pretty fun! Done from Stamford Hospital.

Difficulty: 3.5/10

## Day 4
Word search. Done at home while Katie and Helen watched Thomas <3

Difficulty: 4/10

## Day 5
Create ruleset. Topological sort. Done from Thomas's nursery (at 6am lol)

Difficulty: 5/10

## Day 6
Walk a maze with lookahead. Some real fiddly bits. Done from Thomas's nursery.

Difficulty: 5.5/10

## Day 7
Figure out the operators to solve math equations. Pretty easy to brute force, I just didn't understand Python libraries. Done while Katie was feeding Thomas.

Lesson learned: Be careful about the itertools product/combination/permitation semantics.

Difficulty: 4/10

## Day 8
Draw lines on a grid. 99% there very quickly.

Done on Thomas's first NFL Sunday at home. 

Lesson: Be very careful about floats and equality, and look for areas in libraries where you might have those issues lurking. 

Difficulty: 5.5/10

## Day 9
"Defragment" a giant array. Not conceptually hard but tons and tons of off by ones.

Difficulty: 6/10

## Day 10
Make a digraph, run simple paths over it.

Done from Thomas's nursery.

Difficulty: 4/10

## Day 11
Create an arbitrarily long array. Part 1 was a very literal recreate the array. Part 2 insight was that the order does not matter at all, you can just operate over a histogram.

Difficulty: 5/10

## Day 12
Parse a graph into regions and do things with the regions.
Part 1: 
Find all regions and their sizes. Do that with a BFS.
Find the length of all region borders: you can just iterate over every cell.

Part 2 (spicy): 
Find the *edges*, not the length.
Scan l-r and u-d looking for (top, bottom) and (left, right) edges.
The corner (heh) cases were tricky.

Holiday socks: yellow with Christmas trucks.

Difficulty: 6/10

## Day 13
Solve a system of linear equations. solver makes this only a few lines.

Done after pediatrician visit.

Holiday socks: Bombas

Difficulty: 3.5/10?

## Day 14
Simulate particles moving across a grid. Part 1 very straighforward, part 2 was not my cup of tea. 

Ultimate solution (first time): look for periodicity, once you find it, print all the images that have the right period.
Checked-in solution: Now that I know there is a frame, scan output for '111111"

Difficulty: 5.5/10 (mainly for guess and check on second part.)

## Day 15
Simulate a robot pushing blocks across a grid. Fun coding exercise, and the twist in part two was a great addition. This is a canonically-good AOC puzzle.

Done watching football and chilling with Thomas.
Holiday socks: Running santas.

Difficulty: 7/10

## Day 16
Standard-issue grid navigation problem.

Difficulty: 5/10

## Day 17
OK NOW HERE WE GO WE'RE IN THIS, BABY

An all-time AOC classic and I am really happy with my solution. It's got decompiling assembly. It's got number theory, it's got bit-flips, it slices, it dices.

Done wearing my AOC tshirt! 
Holiday socks: Santa t-rex

Difficulty: 9/10

# Day 18
Recovery day! One that NX can power through.

Difficulty: 6/10

# Day 19
"Match the towels" - fun combinatorics problem 
Awwww yeeeeahhhhh did part 1 in 7 minutes (11 mins e2e) because you can cram the whole thing into a regex. Really happy about that. 

Lessons learned:
- Need to get better at queue/DFS stuff with corner cases. I am not great at debugging these.

In between Thomas feedings. Tree rex tshirt!
pt1 8:43 - 8:54
pt2 9:00ish - 9:29

Difficulty: 7/10

# Day 20
Find your way through a maze but you can teleport one step (then 20 steps in part 2). Fun!

Done from Thomas's nursery after feeding, early in the morning. Tree rex tshirt!

Difficulty: 7/10

# Day 21
OH SHIT HERE WE GO - hardest day of the year. The "control the controller" recursive problem. Complex graph traversal program for part 1 is doable, and then, of course, so much depth that a graph is infeasible for part 2.

Part 1 12/21, but it was a battle. 
Part 2 12/22-12/23, then Christmas break. Finished on 12/27

Solution history:
- Did a "build up the solution" impl which in retrospect was very very close, but didn't have the correct paths for a few of the transitions. Considered hand-coding this (would have worked in retrospect) but ultimately opted for the more robust graph nav approach
- Graph navigation approach - good enough for part 1 and helped with part two. Ultimately very overwrought but them's the breaks. 
- Graph navigation approach with some of the navigation memoized - this got up to depth 16!
- Expand based on the counts of pairs, as each pair expands to the same thing n=2 levels up. THIS SHOULD HAVE WORKED and did in fact work for all known inputs EXCEPT the real input for part 2 :sob:. 
- Rip out graph navigation for keypad nav and do a memoized cost approach, somewhat ripped from reddit. 

Difficulty: 10/10

# Day 22
Make your own crypto algo and then noodle around with it. A blessed reprieve from day 21 (which is fair, but a huge lift).

Done 12/22

Difficulty: 6/10.

# Day 23
Detect cliques in graphs. I banged this out in a half hour. If I knew what various NX calls did it would have been about 10 minutes.

Difficulty: 4/10

# Day 24
Build your own gate sim (part 1) debug a binary adder (part 2). Super fun puzzle. 

My solution is 80% automated. I scan through the adder looking for the correct gates. If there is no gate that meets all the criteria, it barfs. It was easy to ctrl-f to see what the correct gate should have been.

TODO fully automate.

Done 12/26 (part 1) 12/27 (part 2)
Difficulty: 8/10
# Day 25
Done 12/27
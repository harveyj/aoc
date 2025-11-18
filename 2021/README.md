# Advent of Code 2021
## Overview
Started off the year doing the puzzles in Observable notebooks, continuing my 2020 momentum. After a
while got interested in doing Python notebooks, so I switched over to repl.it/notebooks. After some
of the puzzles got computationally intensive I moved to pure Python. 

Started 12/1/2021, finished 1/2/2022. I took 12/23/21 - 12/29/21 almost entirely off so I could
spend time with family. 

## Day 1
Warmup day. JS version was fine, Python rewrite is where I am starting to flex list comprehensions
and feel good.

Location, CT, CT (Python)

Difficulty: 1/10

## Day 2
Still mechanical. JS and Python versions both straightforward. 

Location: CT

Difficulty: 1.5/10

## Day 3
Still pretty straightforward. Bit counting in part 1.

Solution notes: Got part 1 down to three lines which feels pretty good. Probably too compact and
could unpack gamma a bit more but I'll take it. 

Location: CT

Difficulty: 2/10

## Day 4
A little bit of state tracking and logic, but still straightforward. Did the python rewrite in 20-30
minutes. Location: CT

Difficulty: 3.5/10

## Day 5
Python rewrite in about 20 minutes. Writing one set of logic that handles both puzzle cases is
always nice, going back and figuring that out for a few more has been fun.

Difficulty: 3/10

## Day 6
Here we go!! Advent of code starts in earnest. 

Solution notes: I struggled with the initial implementation of part 2 for a while. The breakthrough
was realizing that this is \~= fibonacci numbers, and thus that a dynamic programming approach could
work. Quite happy with the final solution. I have an iterative js solution that I didn't bother to
port.

Difficulty: 6.5/10

## Day 7
A "do you know stats" question - the intuition that you should use mean and median is the key
breakthrough here.

Solution notes: I already forget why I took a micro-brute-force method to part two and I kinda
regret it. 

Difficulty: 4/10

## Day 8
Figure out what number the segment wires are encoding. I got derailed (js edition) for a *long* time
trying to solve the general version of the puzzle, which would have worked. The input very clearly
lets you do a simple logic puzzle version with a long chain of if statements - I eventually bailed
out and took that road. Feels a little like cheating.

Location: CT/CT

Improvements could be: 
* Writing the version that works for arbitrary inputs. 

Difficulty: 5/10

## Day 9
BFS-ish

REWRITE 12/11/24

Difficulty (rewrite): 4/10

## Day 10
Run a stack over a string. Very straightforward, I just needed to read the darn prompt.


REWRITE 12/12/24 Done waiting for Katie's OB appt. Difficulty (rewrite): 3/10

## Day 11
Very straightforward game of life-ish.

REWRITE 12/13/24 with carols, fire, Katie, Thomas

Difficulty (rewrite) 3.5/10

## Day 12
Custom DFS - fun! Nice balance of challenge/algos/thinking.

REWRITE 12/14/24.

Difficulty (rewrite) 5.5/10

## Day 13
"Fold stuff" grid puzzle. Surprisingly straightforward for the middle of AOC.

Difficulty: 5/10

## Day 14
Dynamic programming! "polymerization" extends a string.

Solution notes: It is possible to calculate the number of bigrams in the next step as a function of
the number of bigrams in the previous step. This is because the polymerize step only inserts
characters, so you know that AC insert B yields AB, BC. If it was postfix or prefix you would need
to have the context of where the bigram sat and things would get *way* messier. 

Location: Airplane to CA

Improvements could be:
* Part 1 is just Part 2 but I am leaving Part 1 as-is to show the difference between the approaches. 
* Pull out the answer-finding to a common function.

Difficulty: 6.5/10

## Day 15
Do you know how to graph search: the puzzle. LOTS of corner cases I missed, especially the fact that
cells couldn't be zero, which cost me a good 45 minutes. Being more careful about read the darn
problem is a good note for next year, as is carefully building up the solution.  

Location: Airplane to CA

Improvements would be:
* Combine part one and part two into one thing
* Separate out a grid library

Difficulty: 5/10

## Day 16
Encoding and decoding. I missed some corner cases up front but ultimately not too bad.

Solution notes: This was a "just implement the thing" problem, nothing magical. Trees and recursion
are hard to get the details right on. 

Improvements would be: Pretty happy with this code. 

Location: CA

Difficulty: 5/10

## Day 17
This was the "shoot an item and see if it ends up crossing a zone above/below you" problem. My
solution is really kludge-y looking back on it, this would be a good candidate for a rewrite
eventually. 

Summary: Brute force the you know what out of things. 

Solution notes: If you add 1 to y, the highest point the item reaches is y. A number in the sum of y
needs to fall between apex_y - base_y_1, apex_y - base_y_2.

Location: CA

Improvements would be: A lot of things. 

Difficulty: 6/10

## Day 18
This was a tree descent + mutation / operator application question. The burned extra time quotient
was pretty high for me here - I need to work more on trees. 

Summary: You have a "snailfish number" which is a giant nested list of lists - aka a tree. It is
maximum depth 4 and you add trees by concatenating them. To return to depth 4 you have to spill
numbers over to neighboring nodes.

Solution notes: Model it as a tree, use a standard tree library (this took me too long to get around
to). Construct a list of all of the leaf nodes in order (this also took me too long, I tried to do
everything via up-and-down traversal). 

Libraries: anytree

Location: CA

Improvements would be:
* Pretty happy about the final solution
* A lot of cleanup

Difficulty: 8/10

## Day 19
THIS ONE WAS A BEAST. Second hardest of the year for me, though I got it with no specific hints and
just a "yeah, grind it out" affirmation from reddit. 

Summary: You have a bunch of partially-overlapping but floating in 3d space and uncertain-ly
oriented. You know that they overlap with n=12 points, so use this to reconstruct the connections.

Solution notes: I just did it. It was hard. I started trying to read linear algebra summaries and
then gave up and wrote vectors on an Amazon box and rotated it. Then I checked all my work and found
a few I got wrong. Then, a third time. The coding was easy compared to the mental rotations.

Location: CA

Difficulty: 9/10

Improvements would be:
* I feel pretty happy about the code. 

11/xx/25 
- oh wow, revisitng, and COMPLETE rewrite. the code was a mess! What was four years ago harvey on about?
- the new code finds the adjacent points by intersecting all the vectors over every rotation
- i could probably cache the rotation matrices in the first part and save a factor of 24 on the second loop
- matching the beacons is still the sticking point

## Day 20
I coded the first part quickly and then realized the a-ha and kludged it a *little* bit for part 2. 

Summary: It's Conway's game of life!

Solution notes: Code game of life. The major twist is that the playing board is infinite, and for
the real input value, entirely blank space generates life (but not in the sample value! tricky!).
From there you need to reason through the idea that you have an essentially infinite border which is
blinking on and off every round. I logic-ed this (or kludged it, ymmv) by putting a giant border
around, and just running the standard game of life. 

Location: CA

Difficulty: 6/10 

Improvement would be:
* More principled approach to an infinite board. 

## Day 21
Great example of an AOC puzzle where the solution "feels" right and runs quickly. 

Summary: It's a dice game with moderately complicated rules. The twist in part 2 is that you need to
play out all possible games with all possible dice rolls, with is an exponential explosion. 

Solution notes: Do the first part brute force. "Dirac dice" can be modeled naively (you will never
finish) or by fibonacci / dynamic programming-style calculation, starting from the base state where
one player has just one more point to score. 

f(state) --> # times a wins, # times b wins f(state) --> [outcomes] dot product f(state+outcome)

Location: CA

Improvement would be:
* Cosmetic fixes - I feel good about this one. 

REWRITE NOTES: Rewrote #1 from scratch, much cleaner now.

Difficulty: 8/10

## Day 22
Probably the hardest puzzle of the whole year for me. I had one version that I knew would work but
had so many corner cases I was burning out (cube intersection carefully by hand). I figured out a
much fun-er and simpler but expensive version... which was going to take 12 hours to run. For the
one and only time this year I dipped into the subreddit relatively deeply. 

Giant shoutout to this person, who did what I was doing and made me realize I could pre-filter the
ranges. My answer is very inspired by theirs.
https://www.reddit.com/r/adventofcode/comments/rmivfy/everyone_is_overcomplicating_day_22/

Summary: You have a giant 3-d space and a list of instructions which turn arbitrary cubes in that
space "on" or "off" - figure out how much volume is "on" at the end.

Solution notes: Enumerate every possible x, y, z, divide the universe into grids, check each grid's
lower left corner to see if the last cube to "impact" it was an on or an off. 

Improvement would be:
* Fixing up the cube intersection version which is admittedly the "right" way to do the puzzle.

Location: CA, CA->CT transit. 

Difficulty: 9.5/10

## Day 23
The puzzle-craft in this year's AOC really shone through. This was a great medium-level coding
challenge, with enough corner cases to make things interesting but not a giant slog. 

Summary: Do a towers of hanoi-style shuffle of amphipods into and out of rooms in a narrow corridor.
I accomplished this by treating it as a graph problem, where each node was the complete game state
and each edge was the cost to transition between game states.  

Location: A bit of CT, driving from CT --> VT.

Solution notes: Lowest-cost path through a graph. Part 1 was hand-coded to assume there was only
depth 2, which was kludgey and less general. I'm glad part 2 forced me to rewrite it to be more
general. 

Libraries: networkx

Improvement would be:
* Better graph algorithm - it takes too long to run for my taste.
* Treating all of the As, Bs, etc as interchangeable in all the places I can, which would speed
  things up a bit. 

Difficulty: 7/10

## Day 24
High-quality puzzle and a fitting end to the hard section of Advent of Code. 

Summary: A puzzle that is theoretically about emulating a processor, which turns into a puzzle about
decompiling asssembly, which turns into decoding the and solving the logic puzzle out of decompiled
assembly.

Location: VT, and a car driving from VT --> CT.

Solution notes: I coded up the ALU and wrote a brute force solution quickly, but exp(10, 14) will
take longer than I have time for at the moment. Then I started a very lengthy process of staring at
the ASM, fiddling with values, and trying to figure out the trick. I broke through by transcribing
the ASM to python, then rewriting the Python in-place until it was logically compact. I got it to a
one-liner (plus a loop and constants) but a four-liner was actually the most helpful. I used the ALU
to cross-check my code, then wrote a program to output the answer. 

A-has in rough order
* Write an ALU
* Inspect the code, realize it is broken down into 14 loop-like steps.
* Each loop step can be represented by ($INPUT x, y, z) constants.
* z is the only register that gets carried over from iteration to iteration. 
* Decompile the code into python
* z is basically a stack of numbers 0-26, or a big number written in base 26. 
* In order to get Z down to zero, you need the stack to be empty at the end.
* z div 26 is popping the stack, this happens 7 times. That means that you can have at most 7 pushes
  onto the stack. 
* Any time x_in > 9, you cannot meet the "don't push" criteria. This happens 7 times, so the
  iterations of your 7 stack pushes are fixed. 
* At this point, you have a logic puzzle / constraint puzzle.
* Write a program to show you what the stack looks like at every moment, print out the constraints
  that the stack imposes.
* Evaluate the constraints by hand in a spreadsheet. 

Improvement would be:
* Doing it e2e in code
* Doing it for generic values of the constants / defensively coding it

REDO 11/18/25 on pat leave: made a big mess and then realized i left myself AWESOME notes. Go me!
Once I had the notes, the code became clear, i did it e2e in code! I rewrote the parser to depend on the input! I think this ~= perfect. arbitrary disassembly is not the puzzle - this will work for all inputs which are this shape of puzzle.

Difficulty: 8.5/10

## Day 25
The traditional final state of the Tour De France. I had one or two silly bugs and I had to write a
grid printer to debug them. 

Summary: A really simple game of life / automaton. 

Improvement would be: 
* Optimizing runtime

Difficulty: 3/10
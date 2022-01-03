# Advent of Code 2021
## Overview
Started off the year doing the puzzles in Observable notebooks, continuing my 2020 momentum. After a while got interested in doing Python notebooks, so I switched over to repl.it/notebooks. After some of the puzzles got computationally intensive I moved to pure Python. 

Started 12/1/2021, finished 1/2/2022. I took 12/23/21 - 12/29/21 almost entirely off so I could spend time with family. 

## Day 1
## Day 2
## Day 3
## Day 4
## Day 5
## Day 6
## Day 7
## Day 8
## Day 9
## Day 10
## Day 11
## Day 12
## Day 13
## Day 14
## Day 15
## Day 16
## Day 17
## Day 18
## Day 19
## Day 20
## Day 21
## Day 22
## Day 23
## Day 24
High-quality puzzle and a fitting end to the hard section of Advent of Code. 

Summary: A puzzle that is theoretically about emulating a processor, which turns into a puzzle about decompiling asssembly, which turns into decoding the and solving the logic puzzle out of decompiled assembly.

Location: VT, and a car driving from VT --> CT.

Solution notes: I coded up the ALU and wrote a brute force solution quickly, but exp(10, 14) will take longer than I have time for at the moment. Then I started a very lengthy process of staring at the ASM, fiddling with values, and trying to figure out the trick. I broke through by transcribing the ASM to python, then rewriting the Python in-place until it was logically compact. I got it to a one-liner (plus a loop and constants) but a four-liner was actually the most helpful. I used the ALU to cross-check my code, then wrote a program to output the answer. 

A-has in rough order
* Write an ALU
* Inspect the code, realize it is broken down into 14 loop-like steps.
* Each loop step can be represented by ($INPUT x, y, z) constants.
* z is the only register that gets carried over from iteration to iteration. 
* Decompile the code into python
* z is basically a stack of numbers 0-26, or a big number written in base 26. 
* In order to get Z down to zero, you need the stack to be empty at the end.
* z div 26 is popping the stack, this happens 7 times. That means that you can have at most 7 pushes onto the stack. 
* Any time x_in > 9, you cannot meet the "don't push" criteria. This happens 7 times, so the iterations of your 7 stack pushes are fixed. 
* At this point, you have a logic puzzle / constraint puzzle.
* Write a program to show you what the stack looks like at every moment, print out the constraints that the stack imposes.
* Evaluate the constraints by hand in a spreadsheet. 

Improvement would be:
* Doing it e2e in code
* Doing it for generic values of the constants / defensively coding it

Difficulty: 8/10

## Day 25
The traditional final state of the Tour De France. I had one or two silly bugs and I had to write a grid printer to debug them. 

Summary: A really simple game of life / automaton. 

Improvement would be: 
* Optimizing runtime

Difficulty: 3/10
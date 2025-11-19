# Advent of Code
All puzzles, all years!

## Implementation
- 2015: Complete Python3 implementation.
- 2016: Complete Python3 implementation.
- 2017: Complete Python3 implementation.
- 2018: Completed, but original code was lost to the sands of time. Python3 reimplementation.
- 2019: Complete Python3 implementation.
- 2020: Complete Javascript implementation.
- 2021: Complete Python3 implementation.
- 2022: Complete Python3 implementation.
- 2023: Complete Python3 implementation.
- 2024: Complete Python3 implementation.

## Validation
Validation means that the code spits out the correct answer when one(INPUT) and
two(INPUT) are called. Many days weren't validated because I either solved the
problem in a spreadsheet using the code as an assist, or (more likely) the code
was a mess, spewed out 25 numbers, and I knew at the time which number was the
answer, and I have now forgot. The long-run goal is to go through all the
unvalidated days and give each an interface that spits out the correct day 1,
day 2 answer. 
- 2015: Validated!
- 2016: Validated!
- 2017: Validated!
- 2018: Validated!
- 2019: Validated!
- 2020: Validated!
- 2021: Validated - 17, 22, 23 incorrect
- 2022: Validated - 11 incorrect
- 2023: Validated - 20-2, 21, 23 incorrect
- 2024: Validated!

## Performance hotspots
- 2015: 22-1&2 (3s)
- 2016: 5-1 (5s), 5-2 (14s), 9 (42s), 11-2 (7), 12-2 (30s) 14-2 (30s), 18-2 (40s),
- 2017: 13 (6s), 15-1 (10s), 22-2 (10s), 23-2 (20s), 24 (6s)
- 2018: 14-2 (10s)
- 2019: 23-2 (10s) 24-2 (6s)
- 2020: none (bless you js!)
- 2021: 17, 18-2 (7s), 19 1-2 (17s), 20 (13s), 22 (forever)
- 2022: 16-1 (12s), 20-2 (20s) 23-2 (5s), 24-1 (20s)
- 2023: 17-1 (5s), 18-1 (30s), 23-1 (long), 24-1 (long)
- 2024: 6-2 (13s), 7-2 (8s), 14-2 (6s), 15-2 (13s), 20-1+2 (5s), 22-2 (19s)

## Optimization/cleanup log
- 2015-20 - replaced a not-really-code solution that was 16s with an automated solution that was 3s.
- 2021-21 - rewrote part 1 from scratch, minor cleanup for part 2.
- 2021-09 - rewrote to python
- 2019-19 - full rewrite, really happy, old one was non-functional and i just mashed an answer out of a spreadsheet.
- 2019-20 - full rewrite bc code was a mess
- 2016-23 - partial rewrite/re-solve with more automation and an explanation for how to extract from regs
- 2024-09 - two full rewrites 20s->4s, 4s->1s
- 2018 - complete python reimplementation
- 2015-06 - rewrite to get to 50ms with numpy
- 2016-11 - rewrite with A* to get from "very long" to 10s (pt 1), rewrite again to get to 1s, 7s!
- 2016-24 - rewrite with lazy A*. boom.
- 2016-25 - rewrite.
- 2016-19 - fun rewrite!
- 2017-20 - optimize, validate
- 2018-05 - optimize
- 2019-18 - full rewrite - twice.
- 2019-19 - extensive redo and debug
- 2021-19 - boomshakalaka. one of the hardest AOCs and i got it. 
- 2021-24 - a super fun romp and my notes were great! good job me! 
- 2021-09 - quick rewrite as original had major bug (??)
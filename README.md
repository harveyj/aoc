# Advent of Code
All puzzles, all years!

## Implementation
- 2015: Complete Python3 implementation, standardized
- 2016: Complete Python3 implementation, standardized
- 2017: Complete Python3 implementation, standardized
- 2018: Completed, but original code was lost to the sands of time. Partial Python3 reimplementation.
- 2019: Complete Python3 implementation, standardized
- 2020: Completed in Javascript, standardized
- 2021: Complete Python3 implementation, standardized
- 2022: Complete Python3 implementation, standardized
- 2023: Complete Python3 implementation, standardized
- 2024: Current Python3 implementation, standardized

## Validation
Validation means that the code spits out the correct answer when one(INPUT) and
two(INPUT) are called. Many days weren't validated because I either solved the
problem in a spreadsheet using the code as an assist, or (more likely) the code
was a mess, spewed out 25 numbers, and I knew at the time which number was the
answer, and I have now forgot. The long-run goal is to go through all the
unvalidated days and give each an interface that spits out the correct day 1,
day 2 answer. 
- 2015: Validated - 21 incorrect
- 2016: Validated - 23, 24 unknown, 25 incorrect
- 2017: Validated - 6, 19, 20, 21, 22-25 unknown
- 2018: (not fully implemented)
- 2019: Validated - 18  incorrect
- 2020: Validated - 4-1, 8-1, 10-1, 10-2, 16-1, 18-1, 20-1, 19-1, 19-2, 23-2 incorrect
- 2021: Validated - 9, 16, 17, 19, 20, 21, 22, 23, 24, 25 incorrect
- 2022: Validated - 6, 7, 11, 21, 23, 24, 24 incorrect
- 2023: Validated - 6, 20, 21, 23 incorrect
- 2024: Validated (through day 11)

## Performance hotspots
- 2015: 6-1 (2s), 6-2 (4s), 22-1&2 (3s)
- 2016: 5-1 (5s), 5-2 (14s), 9 (42s), 11 (very long), 12-2 (30s) 14-2 (30s), 18-2 (40s), 19-2 (690s), 24 (very long)
- 2017: 15-1 (10s),  20-1 (50s), 20-2 (30s), 23-2 (20s) 
- 2018: (not fully implemented)
- 2019: 18
- 2020: 23
- 2021: 17, 20
- 2022: 16-1 (12s), 20-2 (20s) 23-2 (5s), 24-1 (20s)
- 2023: 17-1 (5s), 18-1 (30s), 23-1 (long), 24-1 (long)
- 2024: 9-2 (26s)

## Optimization/cleanup log
- 2015-20 - replaced a not-really-code solution that was 16s with an automated solution that was 3s.
- 2021-21 - rewrote part 1 from scratch, minor cleanup for part 2.
- 2021-09 - rewrote to python
- 2019-19 - full rewrite, really happy, old one was non-functional and i just mashed an answer out of a spreadsheet.
- 2019-20 - full rewrite bc code was a mess
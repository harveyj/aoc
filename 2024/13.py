#!/usr/bin/env python3
import puzzle, library
from sympy import symbols, Eq, solve

def parse_input(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  for chunk in chunks:
    a, b, prize = chunk.split('\n')
    yield library.ints(a), library.ints(b), library.ints(prize)

def one(INPUT, two=False):
  all = list(parse_input(INPUT))
  tot = 0
  for a, b, prize in all:
    ax, ay = a; bx, by = b; px, py = prize
    if two: 
      px += 10000000000000; py += 10000000000000
    a_press, b_press = symbols('a, b')
    eq1 = Eq(ax*a_press + bx*b_press, px)
    eq2 = Eq(ay*a_press + by*b_press, py)

    solution = solve([eq1, eq2], (a_press, b_press))
    if int(solution[a_press]) == solution[a_press] and int(solution[b_press]) == solution[b_press]:
      tot += 3 * int(solution[a_press]) + 1 * int(solution[b_press])
  return tot

two = lambda a: one(a, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "13")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

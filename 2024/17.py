#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  a = library.ints(INPUT[0])[0]
  b = library.ints(INPUT[1])[0]
  c = library.ints(INPUT[2])[0]
  prog = list(library.ints(INPUT[4]))
  return a, b, c, prog

def combo(operand, a, b, c):
  if operand in [0,1,2,3]:
    return operand
  elif operand == 4: return a
  elif operand == 5: return b
  elif operand == 6: return c

def iter(a, b, c, prog):
  pc = 0
  out = []
  while pc < len(prog):
    op = prog[pc]
    literal = prog[pc+1]
    combo_val = combo(literal, a, b, c)
    if op == 0: # adv
      a = a // 2**combo_val
      pc += 2
    elif op == 1: # bxl
      b = b ^ literal
      pc += 2
    elif op == 2: # bst
      b = combo_val % 8
      pc += 2
    elif op == 3: # jnz
      if a != 0:
        pc = literal
      else: pc += 2
    elif op == 4: # bxc
      b = b ^ c
      pc += 2
    elif op == 5: # out
      out += [combo_val % 8]
      pc += 2
    elif op == 6: # bdv
      b = a // 2**combo_val
      pc += 2
    elif op == 7: # cdv
      c = a // 2**combo_val
      pc += 2
    else:
      print('ERROR')
  return out

def one(INPUT):
  a, b, c, prog = parse_input(INPUT)
  out = iter(a, b, c, prog)
  return '-'.join(map(str, out))

def program(a):
  return a % 8 ^ 4 ^ (a // 2 ** (a % 8 ^ 1)) % 8

def two(INPUT):
  _, b, c, prog = parse_input(INPUT)
  targets = prog[::-1]
  a = 0
  paths = [a]
  for t in targets:
    new_paths = []
    for a in paths:
      a *= 8
      for i in range(8):
        if program(a+i) == t:
          new_paths.append(a + i)
    paths = new_paths
  return min(paths)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "17")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
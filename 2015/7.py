#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  instrs = []
  for l in INPUT:
    match = re.match('(.*) -> (\w+)', l)
    lval, dest = match.group(1, 2)
    match = re.search('(\w+) (.*) (\w+)', lval)
    if match:
      oper1, op, oper2 = match.group(1, 2, 3)
      # print([oper1, op, oper2, dest])
      if oper2.isdigit():
        oper2 = int(oper2)
      if oper1.isdigit():
        oper1 = int(oper1)
      instrs.append([oper1, op, oper2, dest])
    else:
      match = re.search('(.*) (\w+)', lval)
      if match:
        op, oper2 = match.group(1, 2)
        # print(['NULL', op, oper2, dest])
        instrs.append(['NULL', op, oper2, dest])
      else: 
        match = re.search('(\d+)', lval)
        if match:
          val = match.group(1)
          op = 'SET'
          instrs.append(['NULL', op, int(val), dest])
        else: 
          instrs.append(['NULL', 'ASSIGN', lval, dest])
  return instrs

def apply(v1, op, v2):
  if op == 'AND':
    return v1 & v2
  elif op == 'NOT':
    return ~v2 + 65536
  elif op == 'OR':
    return v1 | v2
  elif op == 'LSHIFT':
    return v1 << int(v2)
  elif op == 'RSHIFT':
    return v1 >> int(v2)
  elif op == 'SET':
    return int(v2)
  elif op == 'ASSIGN':
    return int(v2)
  print('ERROR', v1, op, v2)

# where is c?
def one(INPUT):
  instrs = parse(INPUT)
  registers = {'NULL': 1}
  for i in range(600):
    for inst in instrs:
      v1, op, v2, dest = inst
      val1 = v1 if type(v1) == int else registers.get(v1, None)
      val2 = v2 if type(v2) == int else registers.get(v2, None)
      if val1 != None and val2 != None:
        registers[dest] = apply(val1, op, val2)
  return registers['a']

def two(INPUT):
  return puzzle.Puzzle("2015", "7").run(one, 1)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "7")
  p.run(one, 0)
  p.run(one, 1) # two is one with a different input
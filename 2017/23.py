#!/usr/bin/env python3
import puzzle
from collections import defaultdict

def rewrite_x(xy, regs):
  if xy[0] in regs:
    xy[0] = regs[xy[0]]
  else: xy[0] = int(xy[0])

def rewrite_y(xy, regs):
  if xy[1] in regs:
    xy[1] = regs[xy[1]]
  else: 
    xy[1] = int(xy[1])

class VM(object):
  def __init__(self, instrs):
    self.pc = 0
    self.regs = defaultdict(int)
    self.regs['a'] = 0
    self.regs['b'] = 0
    self.regs['c'] = 0
    self.regs['d'] = 0
    self.regs['e'] = 0
    self.regs['f'] = 0
    self.regs['g'] = 0
    self.regs['h'] = 0
    self.instrs = instrs

  def step(self):
    self.blocking = False
    self.sent = False
    inst = self.instrs[self.pc]
    op, xy = inst.split()[0], inst.split()[1:]
    # print(op, xy)
    if op in ['jnz']:
      rewrite_x(xy, self.regs)
    if op in ['add', 'mul', 'sub', 'jnz', 'set']:
      rewrite_y(xy, self.regs)
    if op in ['add', 'mul', 'sub', 'jnz', 'set']:
      x, y = xy
    else:
      x = xy[0]

    if op == 'set':
      self.regs[x] = y
    elif op == 'add':
      new = self.regs[x] + y
      self.regs[x] = new
    elif op == 'mul':
      new = self.regs[x] * y
      self.regs[x] = new
      self.regs['mul'] += 1
    elif op == 'sub':
      new = self.regs[x] - y
      self.regs[x] = new
    elif op == 'jnz':
      if x != 0:
        # cancel out the += 1 at the end of the loop
        self.pc += y -1
    self.pc += 1


def one(INPUT):
  vm = VM(instrs=INPUT)
  while True:
    vm.step()
    if vm.pc >= len(vm.instrs):
      return vm.regs['mul']
  return 0

def run_vm_two(INPUT):
  vm = VM(instrs=INPUT)
  vm.regs['a'] = 1
  while True:
    if vm.pc == 23:
      print(vm.regs)
    vm.step()
  return 0

def direct_python_translation():
  # direct python translation
  regs = defaultdict(int)

  regs['a'] = 0
  regs['b'] = 0
  regs['c'] = 0
  regs['d'] = 0
  regs['e'] = 0
  regs['f'] = 0
  regs['g'] = 0
  regs['h'] = 0
  regs['a'] = 1

  regs['b'] = 57 # pc = 0
  regs['c'] = regs['b']
  if regs['a'] != 0:
    regs['b'] = regs['b'] * 10 # pc = 4
    regs['b'] = regs['b'] + 100 # pc = 5
    regs['c'] = regs['b'] # pc = 6
    regs['c'] = regs['c'] + 170 # # pc = 7
  while True:
    regs['f'] = 1 # pc = 8
    regs['d'] = 2 # pc = 9
    while True:
      regs['e'] = 2 # pc = 10
      while True:
        regs['g'] = regs['d']
        regs['g'] = regs['g'] * regs['e'] # pc = 12
        regs['g'] = regs['g'] - regs['b'] 
        if regs['g'] == 0:
          regs['f'] = 0
        regs['e'] = regs['e'] + 1
        regs['g'] = regs['e']
        regs['g'] = regs['g'] - regs['b']
        if regs['g'] == 0:
          break
      regs['d'] = regs['d'] + 1
      regs['g'] = regs['d']
      regs['g'] = regs['g'] - regs['b'] 
      # print(regs)
      if regs['g'] == 0:
        break
    if regs['f'] == 0:
      regs['h'] = regs['h'] + 1
      print(regs)
    regs['g'] = regs['b'] 
    regs['g'] = regs['g'] - regs['c'] 
    if regs['g'] == 0:
      break
    regs['b'] = regs['b'] + 17

  print(regs)

def optimized_python():
  regs = defaultdict(int)

  regs['a'] = 0
  regs['b'] = 0
  regs['c'] = 0
  regs['d'] = 0
  regs['e'] = 0
  regs['f'] = 0
  regs['g'] = 0
  regs['h'] = 0
  regs['a'] = 1

  regs['b'] = 57 # pc = 0
  regs['c'] = regs['b']
  if regs['a'] != 0:
    regs['b'] = regs['b'] * 100 # pc = 4
    regs['b'] = regs['b'] + 100000 # pc = 5
    regs['c'] = regs['b'] # pc = 6
    regs['c'] = regs['c'] + 17000 # # pc = 7
  while True:
    regs['f'] = 1 # pc = 8
    regs['d'] = 2 # pc = 9
    while True:
      regs['e'] = 2 # pc = 10
      if 2 <= regs['b'] / regs['d'] < regs['b'] and regs['b'] % regs['d'] == 0:
        regs['f'] = 0
      regs['e'] = regs['b']
      regs['d'] = regs['d'] + 1
      regs['g'] = regs['d']
      regs['g'] = regs['g'] - regs['b'] 
      # print(regs)
      if regs['g'] == 0:
        break
    if regs['f'] == 0:
      regs['h'] = regs['h'] + 1
      print(regs)
    regs['g'] = regs['b'] 
    regs['g'] = regs['g'] - regs['c'] 
    if regs['g'] == 0:
      break
    regs['b'] = regs['b'] + 17
  return regs['h']

def two(INPUT):
  return optimized_python()

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "23")

  p.run(one, 0) 
  p.run(two, 0) 




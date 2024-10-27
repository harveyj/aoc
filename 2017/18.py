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
  def __init__(self, instrs, inbox, outbox):
    self.pc = 0
    self.regs = defaultdict(int)
    self.inbox = inbox
    self.outbox = outbox
    self.instrs = instrs
    self.rcv_called = False # hack for part 1
    self.blocking = False # hack for part 1

  def step(self):
    self.blocking = False
    self.sent = False
    inst = self.instrs[self.pc]
    op, xy = inst.split()[0], inst.split()[1:]
    if op in ['snd', 'jgz']:
      rewrite_x(xy, self.regs)
    if op in ['add', 'mul', 'mod', 'jgz', 'set']:
      rewrite_y(xy, self.regs)
    if op in ['add', 'mul', 'mod', 'jgz', 'set', 'jgz']:
      x, y = xy
    else:
      x = xy[0]
    if op == 'snd':
      self.outbox.append(x)
      self.sent = True
    elif op == 'set':
      self.regs[x] = y
    elif op == 'add':
      new = self.regs[x] + y
      self.regs[x] = new
    elif op == 'mul':
      new = self.regs[x] * y
      self.regs[x] = new
    elif op == 'mod':
      new = self.regs[x] % y
      self.regs[x] = new
    elif op == 'rcv':
      if x != 0 and len(self.inbox) > 0:
        self.regs[x] = self.inbox.pop(0)
        self.rcv_called = True
      else: # block until item in queue
        self.pc -= 1
        self.blocking = True
    elif op == 'jgz':
      if x > 0:
        # cancel out the += 1 at the end of the loop
        self.pc += y -1
    self.pc += 1

def one(INPUT):
  single_queue = []
  vm = VM(instrs=INPUT, inbox=single_queue, outbox=single_queue)
  while True:
    vm.step()
    if vm.rcv_called:
      return single_queue[-1]

def two(INPUT):
  a_out = []
  b_out = []
  vm_a = VM(instrs=INPUT, inbox=b_out, outbox=a_out)
  vm_b = VM(instrs=INPUT, inbox=a_out, outbox=b_out)
  vm_a.regs['p'] = 0
  vm_b.regs['p'] = 1
  total = 0
  while True:
    vm_a.step()
    vm_b.step()
    # if vm_a.sent: 
    #   print('send a', a_out[-1])
    if vm_b.sent: 
      # print('send b', b_out[-1])
      total += 1
    if vm_a.blocking and vm_b.blocking:
      return total

p = puzzle.Puzzle("2017", "18")
p.run(one, 0)
p.run(two, 0)

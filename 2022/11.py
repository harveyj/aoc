#!/usr/bin/env python3
import puzzle
import re

class Monkey:
  PAT = """Monkey (\d+):
  Starting items: (.*)
  Operation: (.*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""

  def __init__(self):
    pass
  
  def parse(self, inval):
    match = re.match(self.PAT, inval)
    self.id = int(match.group(1))
    self.items = [int(val) for val in match.group(2).split(',')]
    self.operation = match.group(3).split('=')[1]
    self.cond = int(match.group(4))
    self.true_monkey = int(match.group(5))
    self.false_monkey = int(match.group(6))
    # print(self.id, self.items, self.operation, self.cond, self.true_monkey, self.false_monkey)
    self.inspect = 0

  
  def receive(self, val):
    self.items.append(val)

def round(monkeys, divide=3, modulo = 1):
  for i in range(len(monkeys)):
    m = monkeys[i]
    while m.items:
      m.inspect += 1
      it = m.items.pop(0)
      # print("Monkey inspects an item with a worry level of", it)
      old = it
      # print("*", m.operation.strip(), "*", sep='')
      new = int(eval(m.operation))
      # print("worry level is ", m.operation, "to", new)
      new = new // divide
      new = new % modulo
      # print("Monkey gets bored with item. Worry level is divided by 3 to", new)
      if new % m.cond == 0:
        # print("Current worry level is divisible by", m.cond)
        monkeys[m.true_monkey].receive(new)
        # print("item with worry level %i is thrown to monkey %s"%(new, m.true_monkey) )
      else: 
        # print("Current worry level is not divisible by", m.cond) 
        monkeys[m.false_monkey].receive(new)
        # print("item with worry level %i is thrown to monkey %s"%(new, m.false_monkey) )

def one(INPUT):
  monkeys = {}
  for l in '\n'.join(INPUT).split('\n\n'):
    m = Monkey()
    m.parse(l)
    monkeys[m.id] = m
  for i in range(20):
    round(monkeys)
  inspects = [monkeys[m].inspect for m in monkeys]
  inspects.sort()
  return inspects[-2] * inspects[-1]

def hash(monkeys):
  return str([[m.id, m.items] for m in monkeys.values()])

def two(INPUT):
  monkeys = {}
  hashes = set()
  for l in '\n'.join(INPUT).split('\n\n'):
    m = Monkey()
    m.parse(l)
    monkeys[m.id] = m
  modulo = 1
  for m in monkeys.values():
    modulo *= m.cond
  for i in range(10000):
    round(monkeys, divide=1, modulo=modulo)
    # h = hash(monkeys)
    # if h in hashes:
    #   print("LOOP", i)
    # else:
    #   print('.', end='')
    #   hashes.add(hash(monkeys))
    # if i % 1000 == 0:
    #   print(i, [monkeys[m].inspect for m in monkeys])
  inspects = [monkeys[m].inspect for m in monkeys]
  inspects.sort()
  return inspects[-2] * inspects[-1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "11")

  p.run(one, 0) 
  p.run(two, 0) 

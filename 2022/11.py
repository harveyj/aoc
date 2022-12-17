#!/usr/bin/env python3
import puzzle
import re

"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Starting items lists your worry level for each item the monkey is currently holding in the order they will be inspected.

Operation shows how your worry level changes as that monkey inspects an item. (An operation like new = old * 5 means that your worry level after the monkey inspected the item is five times whatever your worry level was before inspection.)
Test shows how the monkey uses your worry level to decide where to throw an item next.
If true shows what happens with an item if the Test was true.
If false shows what happens with an item if the Test was false.
After each monkey inspects an item but before it tests your worry level, your relief that the monkey's inspection didn't damage the item causes your worry level to be divided by three and rounded down to the nearest integer.

The monkeys take turns inspecting and throwing items. On a single monkey's turn, it inspects and throws all of the items it is holding one at a time and in the order listed. Monkey 0 goes first, then monkey 1, and so on until each monkey has had one turn. The process of each monkey taking a single turn is called a round.

When a monkey throws an item to another monkey, the item goes on the end of the recipient monkey's list. A monkey that starts a round with no items could end up inspecting and throwing many items by the time its turn comes around. If a monkey is holding no items at the start of its turn, its turn ends.
"""
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
    print(self.id, self.items, self.operation, self.cond, self.true_monkey, self.false_monkey)
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
  for l in INPUT.split('\n\n'):
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
  for l in INPUT.split('\n\n'):
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
    if i % 1000 == 0:
      print(i, [monkeys[m].inspect for m in monkeys])
  inspects = [monkeys[m].inspect for m in monkeys]
  inspects.sort()
  return inspects[-2] * inspects[-1]

p = puzzle.Puzzle("11")
# p.run(one, 1)
p.run(two, 0)

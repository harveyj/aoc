#!/usr/bin/env python3
import puzzle
import json


def onetwo(INPUT, two=False):
  def sum_num(inval):
    val = 0
    if type(inval) == type(0):
      return inval
    if type(inval) == type(""):
      return 0
    if two and type(inval) == type({}) and 'red' in inval.values():
      return 0
    keys = range(len(inval)) if type(inval) == type([]) else inval.keys()
    for k in keys: val += sum_num(inval[k])
    return val

  return sum_num(json.loads(INPUT[0]))

def one(INPUT):
  return onetwo(INPUT, two=False)

def two(INPUT):
  return onetwo(INPUT, two=True)

p = puzzle.Puzzle("2015", "12")
p.run(one, 0)
p.run(two, 0)

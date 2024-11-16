#!/usr/bin/env python3
import puzzle
import json


def onetwo(INPUT):
  def sum_num(inval):
    val = 0
    print(type(inval))
    if type(inval) == type(0):
      return inval
    if type(inval) == type(""):
      return 0
    # Comment this out for part one
    if type(inval) == type({}) and 'red' in inval.values():
      return 0
    keys = range(len(inval)) if type(inval) == type([]) else inval.keys()
    for k in keys: val += sum_num(inval[k])
    return val

  return sum_num(json.loads(INPUT))

p = puzzle.Puzzle("2015", "12")
p.run(onetwo, 0)

#!/usr/bin/env python3
import puzzle
from typing import Any, Tuple
import library
from functools import lru_cache

ELEMENTS = {'promethium':'Pr',
            'cobalt':'Co',
            'ruthenium':'Ru',
            'curium':'Cu',
            'plutonium':'Pu',
            'lithium': 'Li',
            'hydrogen': 'Hg',
            'dilithium': 'Di',
            'elerium': 'El'
            }

def parse(INPUT):
  items = []
  for i, l in enumerate(INPUT):
    for k in ELEMENTS.keys():
      if k+' ' in l: items.append((i, ELEMENTS[k] + '-G'))
      if k+'-' in l: items.append((i, ELEMENTS[k] + '-M'))
  return frozenset(items)

def legal(items):
  oob = [it for it in items if it[0] < 0 or it[0] > 3]
  if oob: return False
  for fl_idx in range(4):
    f = [it[1] for it in items if it[0] == fl_idx]
    unpaired = False; generator = False
    for item in f:
      name = item.split('-')[0]
      unpaired |= name+'-M' in f and not name+'-G' in f
      generator |= name+'-G' in f
    if unpaired and generator:
      return False
  return True

def print_state(state):
  levels = {v:k for k, v in state[1]}
  for k in sorted(levels.keys()): print(k, levels[k], end=' ')
  print('')

def one(INPUT):
  # need a better function
  def h(state):
    fl_idx, items = state
    need_move = {it for it in items if it[0] != 3}
    return max(0, sum([3-c[0] * 2 for c in need_move]) - 3)
  def neighbors(state):
    fl_idx, items = state
    fl_items = {it for it in items if it[0] == fl_idx}
    other_items = {it for it in items if it[0] != fl_idx}
    checked = set()
    for it_a in fl_items:
      ret = {it for it in fl_items if it != it_a }| set([(it_a[0] - 1, it_a[1])]) | other_items
      if legal(ret): yield (fl_idx-1, frozenset(ret))
      ret = {it for it in fl_items if it != it_a }| set([(it_a[0] + 1, it_a[1])]) | other_items
      if legal(ret): yield (fl_idx+1, frozenset(ret))
      checked.add(it_a)
      for it_b in fl_items:
        if it_b in checked: continue
        ret = {it for it in fl_items if it not in [it_a, it_b]} | set([(it_a[0] - 1, it_a[1]), (it_b[0] - 1, it_b[1])]) | other_items
        if legal(ret): yield (fl_idx - 1, frozenset(ret))
        ret = {it for it in fl_items if it not in [it_a, it_b]} | set([(it_a[0] + 1, it_a[1]), (it_b[0] + 1, it_b[1])]) | other_items
        if legal(ret): yield (fl_idx + 1, frozenset(ret))
    return []

  state = (0, parse(INPUT))
  goal = (3, frozenset((3, item[1]) for item in state[1]))
  path = library.a_star_lazy(goal, state, h, neighbors)
  for p in path:
    print(p)
    print_state(p)
  print(len(path) - 1)
  return len(path) - 1

def two(INPUT):
  INPUT[0] += " elerium generator and a elerium-compatible microchip dilithium generator dilithium-compatible microchip"
  return one(INPUT)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "11")
  p.run(one, 0)
  p.run(two, 0)

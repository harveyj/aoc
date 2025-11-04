#!/usr/bin/env python3
import puzzle
import library
from dataclasses import dataclass
import re
import copy

@dataclass(order=True)
class Element:
  g: int
  m: int

def parse(INPUT):
  items = {}
  for i, l in enumerate(INPUT):
    gens = re.findall(r'(\w+) generator', l)
    for k in gens:
      if k in items: items[k].g = i
      else: items[k] = Element(g=i, m=-1)
    micros = re.findall(r'(\w+)-', l)
    for k in micros:
      if k in items: items[k].m = i
      else: items[k] = Element(m=i, g=-1)
  return sorted(items.values())

def legal(fl_idx, items):
  unpaired_m = {e.m for e in items if e.g != e.m}
  g = {e.g for e in items}
  return 0 <= fl_idx < 4 and not unpaired_m.intersection(g)


def one(INPUT):
  def h(state):
    fl_idx, items = state
    m_height = [it.m for it in items if it.m != 3]
    g_height = [it.g for it in items if it.g != 3]
    return max(0, 3 * 2 * len(items) - sum(m_height) - sum(g_height) - 2)
  
  def move_indices(fl_idx, items):
    for delta in [-1, 1]:
      for i in range(len(items) * 2):
        if (i % 2 == 0 and items[i//2].g == fl_idx or
            i % 2 == 1 and items[i//2].m == fl_idx):
          yield (delta, (i,))
      for i in range(len(items) * 2):
        if (i % 2 == 0 and items[i//2].g == fl_idx or
            i % 2 == 1 and items[i//2].m == fl_idx):
          for j in range(i+1, len(items) * 2):
            if (j % 2 == 0 and items[j//2].g == fl_idx or
                j % 2 == 1 and items[j//2].m == fl_idx):
              yield (delta, (i, j))

  def neighbors(state):
    fl_idx, items = state
    for (delta, moves) in move_indices(fl_idx, items):
      new_items = copy.deepcopy(items)
      for m in moves:
        move_g = m % 2 == 0
        if move_g: new_items[m//2].g += delta
        else: new_items[m//2].m += delta
      new_state = (fl_idx + delta), sorted(new_items)
      if legal(*new_state): yield new_state
    return []

  start = parse(INPUT)
  state = (0, start)
  goal = (3, [Element(3, 3) for _ in range(len(start))])
  path = library.a_star_lazy(state, goal, h, neighbors)
  return len(path) - 1

def two(INPUT):
  INPUT[0] += " elerium generator and a elerium-compatible microchip dilithium generator dilithium-compatible microchip"
  return one(INPUT)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "11")
  p.run(one, 0)
  p.run(two, 0)

#!/usr/bin/env python3
import puzzle, re, library, copy
from collections import defaultdict
import networkx as nx
import itertools

def transitions_dirdir():
  return (('^', 'A', '>', 1),
          ('^', 'v', 'v', 1),
          ('A', '^', '<', 1),
          ('A', '>', 'v', 1),
          ('>', 'v', '<', 1),
          ('>', 'A', '^', 1),
          ('v', '>', '>', 1),
          ('v', '^', '^', 1),
          ('v', '<', '<', 1),
          ('<', 'v', '>', 1),
          )

TRANS_DIRDIR = {}

def transitions_dirkey():
  return (('7', '8', '>', 1),
          ('7', '4', 'v', 1),
          ('8', '7', '<', 1),
          ('8', '9', '>', 1),
          ('8', '5', 'v', 1),
          ('9', '8', '<', 1),
          ('9', '6', 'v', 1),
          ('4', '7', '^', 1),
          ('4', '5', '>', 1),
          ('4', '1', 'v', 1),
          ('5', '8', '^', 1),
          ('5', '4', '<', 1),
          ('5', '6', '>', 1),
          ('5', '2', 'v', 1),
          ('6', '9', '^', 1),
          ('6', '5', '<', 1),
          ('6', '3', 'v', 1),
          ('1', '4', '^', 1),
          ('1', '2', '>', 1),
          ('2', '5', '^', 1),
          ('2', '1', '<', 1),
          ('2', '3', '>', 1),
          ('2', '0', 'v', 1),
          ('3', '6', '^', 1),
          ('3', '2', '<', 1),
          ('3', 'A', 'v', 1),
          ('0', '2', '^', 1),
          ('0', 'A', '>', 1),
          ('A', '3', '^', 1),
          ('A', '0', '<', 1))

def follow(graph, path, depth=2):
  move_map_dirdir = {(dir, fr): to for (fr, to, dir, _) in transitions_dirdir()}
  move_map_dirkey = ({(dir, fr): to for (fr, to, dir, _) in transitions_dirkey()})

  state = ('A',) * (depth+1)
  state_path = [state]
  for c in path:
    print(f'from: {state}, {c} ', end='')
    if c == 'A':
      i = 0
      while i < len(state) and state[i] == 'A': i+=1
      if i == depth or i == depth+1:
        print('OUT', state[-1], end= " ")
        if state[-1] == 'A': return
      elif i == depth-1:
        state = (*state[:i+1], move_map_dirkey[(state[i], state[i+1])], *state[i+2:])
      else:
        state = (*state[:i+1], move_map_dirdir[(state[i], state[i+1])], *state[i+2:])
    else:
      state = (move_map_dirdir[(c, state[0])], *state[1:])
    state_path.append(state)
    if not graph.has_edge(state_path[-2], state_path[-1]):
      print('MISSING EDGE', state_path[-2], state_path[-1])
    else: print(f'to {state}')

# TODO arbitrary depths is probably coming... haha nailed it.
def one(INPUT, depth=2):
  key_DG = nx.DiGraph()
  dir_DG = nx.DiGraph()
  # dir, from : to
  move_map_dirdir = {(dir, fr): to for (fr, to, dir, _) in transitions_dirdir()}
  move_map_dirkey = ({(dir, fr): to for (fr, to, dir, _) in transitions_dirkey()})
  for start, end, dir, weight in transitions_dirkey():
    key_DG.add_edge(start, end, dir=dir, weight=weight)
  for start, end, dir, weight in transitions_dirdir():
    dir_DG.add_edge(start, end, dir=dir, weight=weight)
  graph = nx.DiGraph()
  ALL_KEYCODES = '0123456789A'
  ALL_DIRCODES = 'v^><A'
  for kc in ALL_KEYCODES: graph.add_node('OUT' + kc)
  dircodes_product = itertools.product(ALL_DIRCODES, repeat=depth)
  moves_how = dict()
  for dircodes, keycode in itertools.product(dircodes_product, ALL_KEYCODES):
    state = dircodes + tuple(keycode)
    graph.add_node(state)
    # You can always move the top level
    for move in ALL_DIRCODES:
      if (move, state[0]) in move_map_dirdir:
        new_state = (move_map_dirdir[(move, state[0])],
                       *state[1:]) # any further levels
        graph.add_edge(state, new_state)
        moves_how[(state, new_state)] = move
    for i, item in enumerate(state):
      if i == depth:
        new_state = 'OUT' + state[depth]
        graph.add_edge(state, new_state)
        moves_how[(state, new_state)] = 'A'
      elif item == 'A':
        continue
      else:
        # What happens when you hit 'A'
        if i == depth-1:
            if state[0] == 'A' and (state[i], state[i+1]) in move_map_dirkey: # safe due to i+1
              new_state = (*state[:i+1], # the as, the first non a
                          move_map_dirkey[(state[i], state[i+1])]
                          )
              graph.add_edge(state, new_state)
              moves_how[(state, new_state)] = 'A'
        else:
            if (state[i], state[i+1]) in move_map_dirdir: # safe due to i+1
              new_state = (*state[:i+1], # the as, the first non a
                          move_map_dirdir[(state[i], state[i+1])],
                          *state[i+2:] # any further levels
                          )
              graph.add_edge(state, new_state)
              moves_how[(state, new_state)] = 'A'
        break
  scores = []
  start_node = ('A',) * (depth+1)
  for l in INPUT:
    out = ''
    for c in l:
      sp = nx.shortest_path(graph, start_node, 'OUT'+c)
      start_node = ('A',)*depth + (c,)
      chunk = ''.join([moves_how[(n1, n2)] for n1, n2 in zip(sp, sp[1:])])
      out += chunk
    scores.append(int(l[:-1]) * len(out))
  return sum(scores)
  
def two(INPUT):
  return one(INPUT, depth=25)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

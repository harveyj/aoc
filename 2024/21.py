#!/usr/bin/env python3
import puzzle
from collections import defaultdict
import networkx as nx
import itertools
from functools import lru_cache

# Heavily indebted to AoC reddit and https://git.sr.ht/~murr/advent-of-code/tree/master/item/2024/21/p2.py

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


def transitions_dirdir2():
  return (('>', '>', 'A'), 
          ('<', '<', 'A'), 
          ('^', '^', 'A'), 
          ('v', 'v', 'A'), 
          ('A', 'A', 'A'), 

          ('^', 'A', '>A'),
          ('^', 'v', 'vA'),
          ('A', '^', '<A'),
          ('A', '>', 'vA'),
          ('>', 'v', '<A'),
          ('>', 'A', '^A'),
          ('v', '>', '>A'),
          ('v', '^', '^A'),
          ('v', '<', '<A'),
          ('<', 'v', '>A'),

          ('^', '>', 'v>A'),
          ('^', '<', 'v<A'),
          ('>', '^', '<^A'),
          ('>', '<', '<<A'),
          ('<', '>', '>>A'),
          ('v', 'A', '^>A'),
          ('A', 'v', '<vA'),
          ('<', '^', '>^A'),
  
          ('A', '<', 'v<<A'),
          ('<', 'A', '>>^A'), 
          )

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

DIRMAP = {(a, b): c for (a, b, c) in transitions_dirdir2()}

ALL_KEYCODES = '0123456789A'
ALL_DIRCODES = 'v^><A'

def gen_move_graph(depth):
  key_DG = nx.DiGraph()
  dir_DG = nx.DiGraph()
  # dir, from : to
  move_map_dirdir = {(dir, fr): to for (fr, to, dir, _) in transitions_dirdir()}
  move_map_dirkey = ({(dir, fr): to for (fr, to, dir, _) in transitions_dirkey()})
  for start, end, dir, weight in transitions_dirkey():
    key_DG.add_edge(start, end, dir=dir, weight=weight)
  for start, end, dir, weight in transitions_dirdir():
    dir_DG.add_edge(start, end, dir=dir)
  graph = nx.DiGraph()
  for kc in ALL_KEYCODES: graph.add_node('OUT' + kc)
  dircodes_product = itertools.product(ALL_DIRCODES, repeat=depth)
  for dircodes, keycode in itertools.product(dircodes_product, ALL_KEYCODES):
    state = dircodes + tuple(keycode)
    graph.add_node(state)
    # You can always move the top level
    for move in ALL_DIRCODES:
      if (move, state[0]) in move_map_dirdir:
        new_state = (move_map_dirdir[(move, state[0])],
                       *state[1:]) # any further levels
        graph.add_edge(state, new_state, how=move)
    for i, item in enumerate(state):
      if i == depth:
        new_state = 'OUT' + state[depth]
        graph.add_edge(state, new_state, how='A')
        graph.add_edge(new_state, state, how='')
      elif item == 'A':
        continue
      else:
        # What happens when you hit 'A'
        if i == depth-1:
            if (state[i], state[i+1]) in move_map_dirkey: # safe due to i+1
              new_state = (*state[:i+1], # the as, the first non a
                          move_map_dirkey[(state[i], state[i+1])]
                          )
              graph.add_edge(state, new_state, how='A')
        else:
            if (state[i], state[i+1]) in move_map_dirdir: # safe due to i+1
              new_state = (*state[:i+1], # the as, the first non a
                          move_map_dirdir[(state[i], state[i+1])],
                          *state[i+2:] # any further levels
                          )
              graph.add_edge(state, new_state, how='A')
        break
  return graph

def shortest_path(graph, depth, l):
  start_node = ('A',) * (depth+1)
  dir_chunks = []
  path = []
  for c in l:
    sp = nx.shortest_path(graph, start_node, 'OUT'+c)
    start_node = ('A',)*depth + (c,)
    chunk = ''.join([graph.get_edge_data(n1, n2)['how'] for n1, n2 in zip(sp, sp[1:])])
    dir_chunks.append(chunk)
    path += sp
  return ''.join(dir_chunks), path


@lru_cache(maxsize=None)
def get_path(graph, start_node, tgt_node):
  return nx.shortest_path(graph, start_node, tgt_node)

# somewhat confusing but level starts at 0, at the keypad
def get_moves_at_level(graph, path, level):
  arbitrary_node = path[0]
  level_bottom = len(arbitrary_node)-level-1
  moves = [(graph.get_edge_data(n1, n2)['how'], n1, n2) for n1, n2 in zip(path, path[1:])]
  activations = [move for move in moves if move[0] == 'A']
  correct_level = [move for move in activations if ''.join(move[1])[:level_bottom-1] == 'A'*(level_bottom-1)]
  extracted_moves = [move[1][level_bottom-1] for move in correct_level]
  return extracted_moves

@lru_cache
def cost(path, depth):
  if depth == 1:
    # print(path, list(itertools.pairwise('A'+path)))
    return sum([len(DIRMAP[a, b]) for a, b in itertools.pairwise('A'+path)])
  else:
    return sum(cost(DIRMAP[a, b], depth-1) for a, b in itertools.pairwise('A'+path))

def one(INPUT):
  graph4 = gen_move_graph(4)
  out = 0
  for l in INPUT:
    _, sp4 = shortest_path(graph4, 4, l)
    dirs = ''.join(get_moves_at_level(graph4, sp4, 0))
    out += cost(dirs, 2) * int(l[:-1])
  return out

def two(INPUT):
  graph4 = gen_move_graph(4)
  out = 0
  for l in INPUT:
    _, sp4 = shortest_path(graph4, 4, l)
    dirs = ''.join(get_moves_at_level(graph4, sp4, 0))
    out += cost(dirs, 25) * int(l[:-1])
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

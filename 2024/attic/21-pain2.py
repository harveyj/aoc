#!/usr/bin/env python3
import puzzle
from collections import defaultdict
import networkx as nx
import itertools
from functools import lru_cache
from types import MappingProxyType

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

ALL_KEYCODES = '0123456789A'
ALL_DIRCODES = 'v^><A'

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

def gen_move_graph(depth):
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
            if (state[i], state[i+1]) in move_map_dirkey: # safe due to i+1
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
  return graph, moves_how

def shortest_path(graph, moves_how, depth, l):
  start_node = ('A',) * (depth+1)
  path = []
  for c in l:
    sp = nx.shortest_path(graph, start_node, 'OUT'+c)
    start_node = ('A',)*depth + (c,)
    chunk = ''.join([moves_how[(n1, n2)] for n1, n2 in zip(sp, sp[1:])])
    path.append(chunk)
  return path

# TODO arbitrary depths is probably coming... haha nailed it.
def one(INPUT, depth=2):
  total = 0
  graph, moves_how = gen_move_graph(depth)
  for l in INPUT:
    path = shortest_path(graph, moves_how, depth, l)
    total += int(l[:-1]) * len(''.join(path))
  return total

def gen_dir_move_graph(depth):
  dir_DG = nx.DiGraph()
  # dir, from : to
  move_map_dirdir = {(dir, fr): to for (fr, to, dir, _) in transitions_dirdir()}
  for start, end, dir, weight in transitions_dirdir():
    dir_DG.add_edge(start, end, dir=dir, weight=weight)
  graph = nx.DiGraph()
  dircodes_product = itertools.product(ALL_DIRCODES, repeat=depth)
  moves_how = dict()
  for state in dircodes_product:
    graph.add_node(state)
    # You can always move the top level
    for move in ALL_DIRCODES:
      if (move, state[0]) in move_map_dirdir:
        new_state = (move_map_dirdir[(move, state[0])],
                       *state[1:]) # any further levels
        graph.add_edge(state, new_state)
        moves_how[(state, new_state)] = move
    for i, item in enumerate(state):
      if i == depth-1:
        new_state = 'OUT' + state[depth-1]
        graph.add_edge(state, new_state)
        moves_how[(state, new_state)] = 'A'
      elif item == 'A':
        continue
      else:
        # What happens when you hit 'A'
          if (state[i], state[i+1]) in move_map_dirdir: # safe due to i==depth check above
            new_state = (*state[:i+1], # the as, the first non a
                        move_map_dirdir[(state[i], state[i+1])],
                        *state[i+2:] # any further levels
                        )
            graph.add_edge(state, new_state)
            moves_how[(state, new_state)] = 'A'
          break
  return graph, moves_how

def get_moves(path, moves_how):
  return tuple(moves_how[(n1, n2)] for n1, n2 in zip(path, path[1:])) + ('A',) # TODO hack oh no

@lru_cache(maxsize=None)
def get_path(graph, start_node, tgt_node):
  return nx.shortest_path(graph, start_node, tgt_node)

# Hits a wall around n=16
def two_memoize(inval):
  depth = 2
  seq = list(inval)
  graph, moves_how = gen_dir_move_graph(depth)
  for i in range(1):
    new_seq = []
    prev = 'A'
    for cur in seq:
      start_node = (*('A',), prev)
      tgt_node = ('OUT'+cur)
      new_seq += get_moves(tuple(get_path(graph, start_node, tgt_node)), moves_how)
      prev = cur
    seq = new_seq
  return ''.join(seq)

def expand_pair_counts(graph, moves_how, a, b):
  start_node = (*('A',), a)
  tgt_node = ('OUT'+b)
  moves = get_moves(tuple(get_path(graph, start_node, tgt_node)), moves_how)
  new_counts = defaultdict(int)
  prev = 'A'
  for move in moves:
    new_counts[(prev, move)] += 1
    prev = move
  return new_counts

def gen_pair_counts(seq):
  pair_counts = defaultdict(int)
  prev = 'A'
  for cur in seq:
    pair_counts[(prev, cur)] += 1
    prev = cur
  return pair_counts

def expand(seq, graph, moves_how, steps):
  pair_counts = gen_pair_counts(seq)
  for d in range(steps//2):
    new_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
      new_counts = expand_pair_counts(graph, moves_how, pair[0], pair[1])
      for new_pair, new_count in new_counts.items():
        new_pair_counts[new_pair] += count * new_count
    pair_counts = new_pair_counts
  return pair_counts

def check_counts(counts, counts2):
  for key in counts:
    if counts[key] != counts2[key]:
      print('ERROR ', key, counts[key], counts2[key])

def two_counts(INPUT):
  graph, moves_how = gen_dir_move_graph(2)
  graph3, moves_how3 = gen_move_graph(3)
  graph4, moves_how4 = gen_move_graph(4)
  graph5, moves_how5 = gen_move_graph(5)
  moves_how = MappingProxyType(moves_how)

  # for seq in INPUT:
  #   l5_seq = ''.join(shortest_path(graph5, moves_how5, 5, seq))
  #   l5_counts = gen_pair_counts(l5_seq)
  #   l3_seq = ''.join(shortest_path(graph3, moves_how3, 3, seq))
  #   const_pair_counts = expand(l3_seq, graph, moves_how, steps=2)
  #   check_counts(l5_counts, const_pair_counts)

  for seq in ['<A^A>^^AvvvA']:
    l3_seq = ''.join(shortest_path(graph3, moves_how3, 3, seq))
    l3_counts = gen_pair_counts(l3_seq)
    l4_seq = ''.join(shortest_path(graph4, moves_how4, 4, seq))
    l4_counts = gen_pair_counts(l4_seq)
    for key in l3_counts:
      print(key, l3_counts[key], l4_counts[key])

  return
  for seq in INPUT:
    l5_seq = ''.join(shortest_path(graph5, moves_how5, 5, seq))
    l5_counts = gen_pair_counts(l5_seq)
    l5_seq = ''.join(shortest_path(graph5, moves_how5, 5, seq))
    l5_counts = gen_pair_counts(l5_seq)

  for seq in ['<A^A>^^AvvvA']:
    print(graph.nodes)
    l2_seq = ''.join(shortest_path(graph, moves_how, 1, seq))
    print(l2_seq)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two_counts, 0)}')

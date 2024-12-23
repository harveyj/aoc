#!/usr/bin/env python3
import puzzle, re, library, copy
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

def shortest_path_state(graph, moves_how, depth, start_node, end_node):
  sp = nx.shortest_path(graph, start_node, end_node)
  return [moves_how[(n1, n2)] for n1, n2 in zip(sp, sp[1:])]

# TODO arbitrary depths is probably coming... haha nailed it.
def one(INPUT, depth=2):
  total = 0
  graph, moves_how = gen_move_graph(depth)
  for l in INPUT:
    path = shortest_path(graph, moves_how, depth, l)
    total += int(l[:-1]) * len(''.join(path))
  return total
  
def two_blah(INPUT):
  cost_dirdir = {(fr, to): 0 for (fr, to, dir, _) in transitions_dirdir()}
  cost_dirkey = {(fr, to): 0 for (fr, to, dir, _) in transitions_dirkey()}
  cost_dirkey = [('5', '4')]
  start_depth = 2
  graph_n_1, moves_how_n_1 = gen_move_graph(start_depth-1)
  for depth in range(start_depth, start_depth+4):
    print(f'depth {depth}')
    graph, moves_how = gen_move_graph(depth)
    for fr, to in cost_dirkey:
      sp_n_1 = shortest_path(graph_n_1, moves_how_n_1, depth-1, fr+to)[1]
      sp_n = shortest_path(graph, moves_how, depth, fr+to)[1]
      print(sp_n.count('A'))
      print(f'fr {fr}, to {to}, depth{depth-1} {len(sp_n_1)}, depth{depth} {len(sp_n)}')
    graph_n_1 = graph; moves_how_n_1 = moves_how

@lru_cache(maxsize=None)
def cost(graph, start, target, max_depth, layers_above):
  if max_depth == layers_above +1:
    return nx.shortest_path(start, target)

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

def shortest_path_dir(graph, moves_how, depth, l):
  start_node = ('A',) * (depth)
  path = []
  for c in l:
    end_node = ('A',)*(depth-1) + (c,)
    sp = nx.shortest_path(graph, start_node, c)
    start_node = end_node
    chunk = ''.join([moves_how[(n1, n2)] for n1, n2 in zip(sp, sp[1:])])
    path.append(chunk)
  return path


def get_moves(path, moves_how):
  return tuple(moves_how[(n1, n2)] for n1, n2 in zip(path, path[1:]))

@lru_cache(maxsize=None)
def get_path(graph, start_node, tgt_node):
  return nx.shortest_path(graph, start_node, tgt_node)

## MEMOIZE EVERYTHING WE CAN, hits a wall around n=16
def two_memoize(inval):
  depth = 2
  # seq = list('<A^A>^^AvvvA')
  seq = list(inval)
  graph, moves_how = gen_dir_move_graph(depth)
  # print(graph.nodes)
  for i in range(1):
    new_seq = []
    prev = 'A'
    for cur in seq:
      start_node = (*('A',), prev)
      tgt_node = ('OUT'+cur)
      new_seq += get_moves(tuple(get_path(graph, start_node, tgt_node)), moves_how)
      prev = cur
    seq = new_seq
    print(i*2+2, len(seq))
  return ''.join(seq)

def expand_pair_counts(graph, moves_how, a, b):
  start_node = (*('A',), a)
  tgt_node = ('OUT' + b)
  moves = get_moves(tuple(get_path(graph, start_node, tgt_node)), moves_how)
  new_counts = defaultdict(int)
  for a, b in zip(moves, moves[1:]):
    new_counts[(a, b)] += 1
  return new_counts

def gen_pair_counts(seq):
  pair_counts = defaultdict(int)
  prev = 'A'
  for cur in seq:
    pair_counts[(prev, cur)] += 1
    prev = cur
  return pair_counts

def two(INPUT):
  depth = 2
  seq = '<A^A>^^AvvvA'
  seq = '<A'
  graph, moves_how = gen_dir_move_graph(depth)
  moves_how = MappingProxyType(moves_how)
  pair_counts = gen_pair_counts(seq)
  print(pair_counts)
  for d in range(2, 4, 2):
    new_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
      new_counts = expand_pair_counts(graph, moves_how, pair[0], pair[1])
      for new_pair, new_count in new_counts.items():
        new_pair_counts[new_pair] += count * new_count
    pair_counts = new_pair_counts
  good_pair_counts = gen_pair_counts(two_memoize(seq))
  for key in gen_pair_counts(two_memoize(seq)):
    if good_pair_counts[key] != pair_counts[key]:
      # the two errors are: at the very start, at the gap between the two chars
      print('ERROR ', key, pair_counts[key], good_pair_counts[key])
  good_two = two_memoize(seq)
  print(good_two, gen_pair_counts(good_two))
  # print(sum(pair_counts.values()))
  # print(len('v<A<AA>^>AvAA^<A>Av<<A>^>AvA^Av<A^>A<Av<A>^>AAvA^Av<<A>A^>AAAvA<^A>A'))


if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 1)}')

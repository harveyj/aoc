#!/usr/bin/env python3
import puzzle
from collections import defaultdict
import networkx as nx
import itertools
from functools import lru_cache
from types import MappingProxyType

### LIBRARY - stable functions below

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

def check_counts(counts, counts2):
  print('CHECKING', len(counts), len(counts2))
  for key in counts:
    if counts[key] != counts2[key]:
      print('ERROR ', key, counts[key], counts2[key])

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

###### END LIBRARY

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

def gen_dir_move_graph(depth):
  dir_DG = nx.DiGraph()
  # dir, from : to
  move_map_dirdir = {(dir, fr): to for (fr, to, dir, _) in transitions_dirdir()}
  for start, end, dir, weight in transitions_dirdir():
    dir_DG.add_edge(start, end, dir=dir, weight=weight)
  graph = nx.DiGraph()
  dircodes_product = itertools.product(ALL_DIRCODES, repeat=depth)
  for state in dircodes_product:
    graph.add_node(state)
    # You can always move the top level
    for move in ALL_DIRCODES:
      if (move, state[0]) in move_map_dirdir:
        new_state = (move_map_dirdir[(move, state[0])],
                       *state[1:]) # any further levels
        graph.add_edge(state, new_state, how=move)
    for i, item in enumerate(state):
      if i == depth-1:
        new_state = 'OUT' + state[depth-1]
        graph.add_edge(state, new_state, how='A')
        graph.add_edge(new_state, state, how='')
      elif item == 'A':
        continue
      else:
        # What happens when you hit 'A'
          if (state[i], state[i+1]) in move_map_dirdir: # safe due to i==depth check above
            new_state = (*state[:i+1], # the as, the first non a
                        move_map_dirdir[(state[i], state[i+1])],
                        *state[i+2:] # any further levels
                        )
            graph.add_edge(state, new_state, how='A')
          break
  return graph

def get_moves(graph, path):
  return tuple(graph.get_edge_data(n1, n2)['how'] for n1, n2 in zip(path, path[1:])) + ('A',) # TODO hack oh no


def expand_counts_ab(graph, a, b):
  start_node = (*('A',), a)
  tgt_node = ('OUT'+b)
  moves = get_moves(graph, tuple(get_path(graph, start_node, tgt_node)))
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

# def expand(seq, graph, steps):
#   pair_counts = gen_pair_counts(seq)
#   for d in range(steps//2):
#     new_pair_counts = defaultdict(int)
#     for pair, count in pair_counts.items():
#       new_counts = expand_pair_counts(graph, pair[0], pair[1])
#       for new_pair, new_count in new_counts.items():
#         new_pair_counts[new_pair] += count * new_count
#     pair_counts = new_pair_counts
#   return pair_counts

def expand_counts(dir_graph, pair_counts):
  new_pair_counts = defaultdict(int)
  for pair, count in pair_counts.items():
    new_counts = expand_counts_ab(dir_graph, pair[0], pair[1])
    for new_pair, new_count in new_counts.items():
      new_pair_counts[new_pair] += count * new_count
  return new_pair_counts


# TODO arbitrary depths is probably coming... haha nailed it.
def one(INPUT, depth=2):
  total = 0
  graph = gen_move_graph(depth)
  for l in INPUT:
    path, _ = shortest_path(graph, depth, l)
    total += int(l[:-1]) * len(path)
  return total

def two(INPUT):
  dir_graph = gen_dir_move_graph(2)
  level_up = dict()
  for d1 in ALL_DIRCODES:
    for d2 in ALL_DIRCODES:
      start_node = ('A', d1); tgt_node = 'OUT'+d2
      sp = get_path(dir_graph, start_node, tgt_node)
      seq = get_moves_at_level(dir_graph, sp, 0)
      level_up[(d1, d2)] = gen_pair_counts(seq)
  # TODO need to account for first code - is it always left or down?

  graph4 = gen_move_graph(4)
  graph6 = gen_move_graph(6)
  graph7 = gen_move_graph(7)

  outs = []
  for l in INPUT:
    print('**')
    sp4raw, sp4 = shortest_path(graph4, 4, l)
    sp6raw, sp6 = shortest_path(graph6, 6, l)
    sp7raw, sp7 = shortest_path(graph7, 7, l)
    base = ''.join(get_moves_at_level(graph4, sp4, 0))
    pairs_0 = gen_pair_counts(base)
    pairs = pairs_0
    iters = 5
    for i in range(iters):
      new_pairs = defaultdict(int)
      for key in pairs:
        pair, count = key, pairs[key]
        for sub_pair, sub_pair_count in level_up[pair].items():
          new_pairs[sub_pair] += count * sub_pair_count
      pairs = new_pairs
    correct_moves = ''.join(get_moves_at_level(graph7, sp7, iters))
    correct_pairs = gen_pair_counts(correct_moves)
    check_counts(new_pairs, correct_pairs)
    assert sum(correct_pairs.values()) == sum(pairs.values())
    outs.append(int(l[:-1]) * sum(pairs.values()))
    # print()
  return sum(outs)


def two_new(INPUT):
  dir_graph = gen_dir_move_graph(2)
  level_up = dict()
  for d1 in ALL_DIRCODES:
    for d2 in ALL_DIRCODES:
      start_node = ('A', d1); tgt_node = 'OUT'+d2
      sp = get_path(dir_graph, start_node, tgt_node)
      seq = get_moves_at_level(dir_graph, sp, 0)
      level_up[(d1, d2)] = gen_pair_counts(seq)
  # TODO need to account for first code - is it always left or down?

  graphs = {i: gen_move_graph(i) for i in range(2, 7)}
 
  outs = []
  INPUT = ['029A']
  for l in INPUT:
    print('**')
    shortest_paths = {i: shortest_path(graphs[i], i, l)[1] for i in graphs}
    base = ''.join(get_moves_at_level(graphs[4], shortest_paths[4], 2))
    print(''.join(get_moves_at_level(graphs[3], shortest_paths[3], 2)))
    pairs_0 = gen_pair_counts(base)
    pairs = pairs_0
    print(pairs_0)
    iters = 4
    for i in range(iters):
      new_pairs = defaultdict(int)
      for key in pairs:
        pair, count = key, pairs[key]
        for sub_pair, sub_pair_count in level_up[pair].items():
          new_pairs[sub_pair] += count * sub_pair_count
      pairs = new_pairs
    correct_moves = ''.join(get_moves_at_level(graphs[6], shortest_paths[6], iters))
    correct_pairs = gen_pair_counts(correct_moves)
    # check_counts(new_pairs, correct_pairs)
    # assert sum(correct_pairs.values()) == sum(pairs.values())
    # outs.append(int(l[:-1]) * sum(pairs.values()))
    # print()
  return sum(outs)


# 174275498291374 too high
if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  # print(f'ANSWER: {p.run(one, 1)}')
  print(f'ANSWER: {p.run(two, 0)}')

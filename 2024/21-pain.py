#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx

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
          # ('A', '<', 'v<<', 2.9),
          # ('>', 'A', '>>^', 2.9),
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

def get_subseq(DG, a, b):
  paths = list(nx.all_shortest_paths(DG, a, b, weight='weight'))
  if len(paths) > 1:
    # doubles = [(p, len([a for a, b in zip(p, p[1:]) if a == b])) for p in paths]
    pass
  path = nx.shortest_path(DG, a, b)
  return [DG.get_edge_data(a, b)['dir'] for a, b in zip(path, path[1:])] + ['A']


def fastest_dirpad_pair(dir_DG, a, b, depth):
  if depth == 1:
    return nx.shortest_path(dir_DG, a, b)
  all_paths = []
  for node, prev_node in zip(path, path[1:]):
    seq.append(nx.shortest_path(dir_DG, node, prev_node))
  return seq

def shortest_expansion(dir_DG, path, levels):
  ret = []
  if levels == 1:
    for a, b in zip(path, path[1:]):
      ret += nx.shortest_path(dir_DG, a, b) + ['A']
    return ret
  pass


# def one_scrap(INPUT):
#   key_DG = nx.DiGraph()
#   dir_DG = nx.DiGraph()
#   for start, end, dir, weight in transitions_dirkey():
#     key_DG.add_edge(start, end, dir=dir, weight=weight)
#   for start, end, dir, weight in transitions_dirdir():
#     dir_DG.add_edge(start, end, dir=dir, weight=weight)
#   for l in INPUT:
#     prev_k = 'A'
#     overall_path = []
#     for tgt in l:
#       path_seqs = defaultdict(list) # key = path
#       for path in all_paths(key_DG, prev_k, tgt):
#         path = path + ['A']
#         print(path, prev_k, tgt)
#         for a, b in zip(path, path[1:]):
#           path_seqs[tuple(path)] += fastest_dirpad_pair(dir_DG, a, b, 1)
#       print(path_seqs)
#       min_path = min(path_seqs.values(), key=lambda a: len(a))
#       print(f'best between {prev_k}, {tgt}, {min_path}')
#       overall_path += tuple(min_path)
#       prev_k = tgt
#     print(''.join(overall_path))


def all_paths(DG, a, b):
  paths = nx.all_simple_paths(DG, a, b)
  return [[DG.get_edge_data(a, b)['dir'] for a, b in zip(path, path[1:])] for path in paths]

def one(INPUT):
  key_DG = nx.DiGraph()
  dir_DG = nx.DiGraph()
  for start, end, dir, weight in transitions_dirkey():
    key_DG.add_edge(start, end, dir=dir, weight=weight)
  for start, end, dir, weight in transitions_dirdir():
    dir_DG.add_edge(start, end, dir=dir, weight=weight)
  for l in INPUT:
    prev_k = 'A'
    shortest_steps = {}
    for tgt in l:
      all_ab_expansions = {}
      # path_ab is a candidate path between the numbers on the keypad
      for path_ab in all_paths(key_DG, prev_k, tgt):
        se = shortest_expansion(dir_DG, path_ab, 1)
        print(prev_k, tgt, path_ab + ['A'], 'se', se)
        all_ab_expansions[tuple(path_ab)] = se
      print('min', min(all_ab_expansions.items(), key=lambda a: len(a[1])))
      prev_k = tgt

      # append optimal way of getting from prev_k to tgt
      # optimal way of getting from prev_k to tgt is:
      #  generate all paths of depth d

def two(INPUT):
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "21")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

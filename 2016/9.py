#!/usr/bin/env python3
import puzzle
import networkx as nx

def expand(l):
  out = []
  i = 0
  while i < len(l):
    c = l[i]
    if c == '(':
      s = i; e = i
      while l[e] != ')':
        e += 1
      length, reps = map(int, l[s+1:e].split('x'))
      i = e
      out.append(l[e+1:e+length+1] * reps)
      i += length+1
    else:
      out.append(c)
      i += 1
  return ''.join(out)


def one(INPUT):
  for l in INPUT:
    return len(expand(l))

def expand2(l, DEBUG=False):
  stack = [(0, 0)] # start, depth
  start_to_end = dict()
  start_to_end[(0, 0)] = len(l) 
  tree = nx.DiGraph()
  tree.add_node((0, 0), reps=1) # start, depth
  i = 0
  while i < len(l):
    c = l[i]
    DEBUG and print(f'c{c}')
    while i == start_to_end[stack[-1]]:
      stack.pop()
    if c == '(':
      s = i; e = i
      while l[e] != ')':
        e += 1
      length, reps = map(int, l[s+1:e].split('x'))
      i = e+1
      key = (e+1, len(stack))
      stack.append(key)
      DEBUG and print(f'add: {key, reps}')
      tree.add_node(key, reps=reps)
      DEBUG and print((stack[-2], stack[-1]))
      tree.add_edge(stack[-2], stack[-1])
      start_to_end[key] = e+length + 1
    else:
      key = (i, len(stack))
      DEBUG and print(f'k{key}, s{stack[-1]}, c{c}')
      DEBUG and print(f'add: {key, 1}')
      tree.add_node(key, reps=1, value=1, datum=c)
      tree.add_edge(stack[-1], key)
      start_to_end[key] = i+1
      i += 1
  # thanks, chatgpt...
  for node in nx.dfs_postorder_nodes(tree, (0,0)):
    if tree.out_degree(node) > 0:
      # print(tree.nodes[node]['reps'])
      tree.nodes[node]['value'] = sum(tree.nodes[child]['value'] for child in tree.successors(node)) * tree.nodes[node]['reps']
      tree.nodes[node]['datum'] = ''.join((tree.nodes[child]['datum'] for child in tree.successors(node))) * tree.nodes[node]['reps']

  return tree.nodes[(0,0)]['value']


def two(INPUT):
  for l in INPUT:
    return expand2(l)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "9")

  p.run(one, 0)
  p.run(two, 0)

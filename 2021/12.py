#!/usr/bin/env python3
import puzzle
import networkx as nx

def parse_input(INPUT):
  G = nx.Graph()
  for l in INPUT:
    a, b = l.split('-')
    G.add_node(a)
    G.add_node(b)
    G.add_edge(a, b)
  return G

def custom_DFS_paths(G, start, end, two=False):
  paths = set()
  queue = [(start,)] # path so far
  while queue:
    path = queue.pop()
    for n in G.neighbors(path[-1]):
      if n == start: continue
      if two:
        little = n.lower() == n
        max_count = max([path.count(n2) for n2 in path if n2.lower() == n2])
        my_count = path.count(n)
        if little and max_count > 1 and my_count >= 1: continue
      else:
        if n.lower() == n and n in path: continue
      if n == end:
        paths.add(path+(n,))
        continue
      queue.append(path+(n,))
  return paths

def one(INPUT):
  G = parse_input(INPUT)
  return len(custom_DFS_paths(G, 'start', 'end'))

def two(INPUT):
  G = parse_input(INPUT)
  return len(custom_DFS_paths(G, 'start', 'end', two=True))

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "12")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

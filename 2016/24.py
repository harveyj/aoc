#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib, itertools


def one(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  nodes = dict()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)).isdigit():
        nodes[(x, y)] = G.get((x, y))
  print(nodes)
  graph = nx.Graph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) != '#':
        graph.add_node((x, y))
        for loc, val in G.neighbors_kv((x, y)):
          if val != '#':
            graph.add_edge((loc), (x, y))
  print(graph)
  weights = dict(nx.all_pairs_shortest_path(graph))
  graph2 = nx.Graph()
  for n0 in nodes:
    graph2.add_node(n0)
    for n1 in nodes:
      # fencepost accounts for the -1
      graph2.add_edge(n0, n1, weight=len(weights[n0][n1])-1)
  weights = dict(nx.all_pairs_dijkstra_path_length(graph2, weight='weight'))
  print(weights)
  for n0 in nodes:
    for n1 in nodes:
      print(n0, n1, weights[n0][n1])
  next_nodes = {loc:nodes[loc] for loc in nodes if nodes[loc] != '0'}
  start_node = [loc for loc in nodes if nodes[loc] == '0'][0]
  
  min_total=100000000
  min_path = []
  for path in itertools.permutations(next_nodes):
    total = weights[start_node][path[0]]
    for n0, n1 in zip(path, path[1:]):
      total += weights[n0][n1]
    if True: # Two
      total += weights[n1][start_node]
    if total < min_total:
      min_total = total
      min_path = [start_node] + list(path)
  return min_total, min_path

def two(INPUT):
  return 0

p = puzzle.Puzzle("24")
p.run(one, 0)
p.run(two, 0)

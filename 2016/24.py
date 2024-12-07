#!/usr/bin/env python3
import puzzle, library
import networkx as nx
import itertools


def one(INPUT, two=False):
  G = library.Grid(raw='\n'.join(INPUT))
  nodes = dict()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)).isdigit():
        nodes[(x, y)] = G.get((x, y))
  graph = nx.Graph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) != '#':
        graph.add_node((x, y))
        for loc, val in G.neighbors_kv((x, y)):
          if val != '#':
            graph.add_edge((loc), (x, y))
  weights = dict(nx.all_pairs_shortest_path(graph))
  graph2 = nx.Graph()
  for n0 in nodes:
    graph2.add_node(n0)
    for n1 in nodes:
      # fencepost accounts for the -1
      graph2.add_edge(n0, n1, weight=len(weights[n0][n1])-1)
  weights = dict(nx.all_pairs_dijkstra_path_length(graph2, weight='weight'))

  next_nodes = {loc:nodes[loc] for loc in nodes if nodes[loc] != '0'}
  start_node = [loc for loc in nodes if nodes[loc] == '0'][0]
  
  min_total=100000000
  min_path = []
  for path in itertools.permutations(next_nodes):
    total = weights[start_node][path[0]]
    for n0, n1 in zip(path, path[1:]):
      total += weights[n0][n1]
    if two:
      total += weights[n1][start_node]
    if total < min_total:
      min_total = total
      min_path = [start_node] + list(path)
  return min_total, min_path

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "24")

  p.run(one, 0)
  p.run(two, 0)

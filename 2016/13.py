#!/usr/bin/env python3
import puzzle, library
import networkx as nx

def bits(num):
  ones = 0
  while num > 0:
    ones += num % 2
    num //= 2
  return ones

def is_wall(x, y, favorite):
  prod = x*x + 3*x + 2*x*y + y + y*y + favorite
  return bits(prod) %2 == 1

def make_graph(INPUT):
  favorite = int(INPUT[0])
  G = library.Grid(x=50,y=50)
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if is_wall(x, y, favorite):
        G.set((x, y), '#')
  graph = nx.Graph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      for neighbor in G.neighbors_locs((x,y)):
        if G.get((x, y)) == '.' and G.get(neighbor) == '.':
          graph.add_edge((x, y), neighbor)
  return graph


def one(INPUT):
  graph = make_graph(INPUT)
  dp = nx.dijkstra_path(graph, (1,1), (31, 39))
  return len(dp) - 1 # fencepost off by one

def two(INPUT):
  graph = make_graph(INPUT)
  edges = nx.bfs_edges(graph, (1,1), depth_limit=50)
  nodes = [(1,1)] + [v for u, v in edges]
  return len(nodes)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "13")

  p.run(one, 0)
  p.run(two, 0)

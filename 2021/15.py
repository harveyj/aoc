import puzzle
from collections import defaultdict
import networkx as nx

### Part 1
def process_input(INPUT):
  G = nx.DiGraph()
  grid = [list(line) for line in '\n'.join(INPUT).split('\n')]
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      c = int(c)
      G.add_edge((x, y-1), (x, y), weight=c)
      G.add_edge((x-1, y), (x, y), weight=c)
      G.add_edge((x, y+1), (x, y), weight=c)
      G.add_edge((x+1, y), (x, y), weight=c)
  return G, len(grid[0])-1, len(grid)-1

def one(intext):
  G, max_x, max_y = process_input(intext)
  return nx.dijkstra_path_length(G, (0,0), (max_x, max_y))

### Part 2
def process_input2(INPUT):
  G = nx.DiGraph()
  grid = [list(line) for line in '\n'.join(INPUT).split('\n')]
  max_x = len(grid[0])
  max_y = len(grid)
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      for x_i in range(5):
        for y_i in range(5):
          c = int(c)
          w = (c+x_i+y_i-1)%9+ 1
          G.add_edge((x+x_i*max_x, y-1+y_i*max_y), (x+x_i*max_x, y+y_i*max_y), weight=w)
          G.add_edge((x-1+x_i*max_x, y+y_i*max_y), (x+x_i*max_x, y+y_i*max_y), weight=w)
          G.add_edge((x+x_i*max_x, y+1+y_i*max_y), (x+x_i*max_x, y+y_i*max_y), weight=w)
          G.add_edge((x+1+x_i*max_x, y+y_i*max_y), (x+x_i*max_x, y+y_i*max_y), weight=w)
  return G, len(grid[0])*5-1, len(grid)*5-1

def get_grid(INPUT):
  grid = [list(line) for line in '\n'.join(INPUT).split('\n')]
  max_x = len(grid[0])
  max_y = len(grid)
  ret = {}
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      for x_i in range(5):
        for y_i in range(5):
          c = int(c)
          w = (c+x_i+y_i-1)%9+ 1
          ret[(x + x_i * max_x, y + y_i * max_y)] = w
  return ret

def two(intext):
  G, max_x, max_y = process_input2(intext)
  # print(nx.astar_path_length(G, (0,0), (max_x, max_y)))
  p=nx.astar_path(G, (0,0), (max_x, max_y))
  vals = get_grid(intext)
  grid = [[int(vals[(x, y)]) for x in range(max_x+1)] for y in range(max_y+1)]
  tot = 0
  for x, y in p[1:]:
    tot+=grid[y][x]
  return tot
  # for l in grid:
  #   print(''.join(l))

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "15")

  p.run(one, 0) 
  p.run(two, 0) 

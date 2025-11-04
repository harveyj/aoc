import re, copy
import networkx as nx
from collections import defaultdict
import heapq

# E, S, W, N
DIRS_CARDINAL = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def ints(line):
  return list(map(int, re.findall(r"-?\d+", line)))

def neighbors(pt):
  return tuple(pt_add(pt, d) for d in DIRS_CARDINAL)

def pt_add(pt1, pt2):
  return (pt1[0] + pt2[0], pt1[1] + pt2[1])

def mul_vect(vect, mag):
  return [i * mag for i in vect]

def manhattan(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Grid:

  def __init__(self, x=0, y=0, grid=None, raw=None):
    if raw:
      self.grid=[list(l) for l in raw.split('\n')]
    elif grid:
      self.grid = copy.deepcopy(grid)
    else:
      self.grid = [["." for i in range(x)] for j in range(y)]
    self.overlays = {}
    self.counts = defaultdict(int)
    self.counts['.'] = x * y

  NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  NEIGHBORS_DIAG = NEIGHBORS + [(-1, -1), (1, -1), (1, 1), (-1, 1)]

  def __hash__(self):
    return hash(tuple(map(tuple, self.grid)))

  def __eq__(self, other):
    return self.__hash__() == other.__hash__()

  def max_x(self):
    return len(self.grid[0])

  def max_y(self):
    return len(self.grid)

  def set(self, pt, val):
    x, y = pt
    self.counts[self.get(pt)] -= 1
    self.counts[val] += 1
    self.grid[y][x] = val

  def get(self, pt, default=None):
    x, y = pt
    if x < 0 or y < 0 or x >= self.max_x() or y >= self.max_y():
      return default
    return self.grid[y][x]

  def get_repeating(self, pt):
    return self.get(((pt[0] % self.max_x()), (pt[1] % self.max_y())))

  def legal(self, pt):
    return 0 <= pt[0] < self.max_x() and 0 <= pt[1] < self.max_y()

  def detect_fast(self, val):
    return self.counts[val]

  def detect(self, val):
    return [(x, y) 
            for x in range(self.max_x()) for y in range(self.max_y())
            if self.get((x, y)) == val]

  def neighbors(self, pt):
    x, y = pt
    return filter(
        lambda a: a != None,
        [self.get((x + DX, y + DY)) for DX, DY in self.NEIGHBORS],
    )

  def neighbors_default(self, pt, default='.'):
    x, y = pt
    return [self.get((x + DX, y + DY), default=default) for DX, DY in self.NEIGHBORS]

  def neighbors_kv(self, pt, default=None):
    x, y = pt
    return filter(
        lambda a: a != None,
        [(((x + DX), (y+DY)), self.get((x + DX, y + DY), default=default)) for DX, DY in self.NEIGHBORS],
    )

  def neighbors_diag(self, pt):
    x, y = pt
    return filter(
        lambda a: a != None,
        [self.get((x + DX, y + DY)) for DX, DY in self.NEIGHBORS_DIAG],
    )

  def neighbors_locs(self, pt):
    x, y = pt
    return [(x + DX, y + DY) for DX, DY in self.NEIGHBORS]

  def neighbors_diag_locs(self, pt):
    x, y = pt
    return [(x + DX, y + DY) for DX, DY in self.NEIGHBORS_DIAG]

  def __str__(self):
    rows = []
    for y, row in enumerate(self.grid):
      row_out = []
      for x, cell in enumerate(row):
        if (x, y) in self.overlays:
          row_out.append(self.overlays[(x, y)])
        else:
          row_out.append(cell)
      rows.append(''.join(map(str, row_out)))
    return '\n'.join(rows)

  def window(self, min_x, min_y, max_x, max_y):
    grid = [row[min_x:max_x] for row in self.grid[min_y:max_y]]
    for (x, y) in self.overlays:
      if x < max_x and y < max_y and x >= min_x and y >= min_y:
        grid[y-min_y][x-min_x] = self.overlays[(x, y)]

    return '\n'.join(
        [''.join(row) for row in grid])
  
  def graph(self, permissible='SE.'):
    G = nx.Graph()
    for x in range(self.max_x()):
      for y in range(self.max_y()):
        c = self.get((x, y))
        for pt, val in self.neighbors_kv((x, y), default='#'):
          if c in permissible and val in permissible:
            G.add_edge(pt, (x, y))
    return G


# input: a continuation / iter that yields (i, state)
# input: a function that takes state, outputs score
# output: the offset at which the periodicity begins, the delta per iteration
def detect_steady_state(fn, score):
  prev_delt = -100000
  last = 0
  for (i, state) in fn:
    new = score(state)
    delt = new - last
    if delt == prev_delt:
      return i, new, delt
    last = new
    prev_delt = delt

# input: a continuation / iter that yields (i, state)
# output: the offset at which the periodicity begins, the value at that point, the delta per iteration
def find_period(fn):
  cache = dict()
  for (i, state) in fn:
    state = str(state)
    if state in cache:
      period = i - cache[state]
      break
    cache[state] = i
  return i, period

def find_periodic_state_at(fn, minimum, period, tgt):
  for (i, state) in fn:
    if i > minimum and (tgt-i) % period == 0:
      return state

def a_star_lazy(start, goal, h, neighbors):
  def reconstruct_path(came_from, current):
    total_path = [current]
    while str(current) in came_from.keys():
      current = came_from[str(current)]
      total_path.insert(0, current)
    return total_path
  open_set = [(h(start), start)]
  came_from = dict()
  g_score = defaultdict(lambda: 1000000000)
  g_score[str(start)] = 0
  f_score = {str(start):h(start)}
  while open_set:
    current = heapq.heappop(open_set)[1]
    if current == goal:
      return reconstruct_path(came_from, current)
    for n in neighbors(current):
      tentative_gScore = g_score[str(current)] + 1
      if tentative_gScore < g_score[str(n)]:
        came_from[str(n)] = current
        g_score[str(n)] = tentative_gScore
        f_score[str(n)] = tentative_gScore + h(n)
        if n not in open_set:
          heapq.heappush(open_set, ((f_score[str(n)], n)))
  return None

def test_a_star():
  def simple_neighbors(n):
    for i in range(len(n)):
      if n[i] > 5: continue
      yield n[:i] + (n[i]+1,) + n[i+1:]

  def h(state):
    return 3 * len(state) - sum(state)

  path = a_star_lazy((0,0,0), (3, 2, 1), h, simple_neighbors)
  for p in path:
    print(p)


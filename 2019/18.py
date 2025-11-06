#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict
from functools import lru_cache, partial

def neighbors_ptpt(G, goal, loc):
  for new_loc, val in G.neighbors_kv(loc, default='#'):
    if val in [goal, '.']:
      yield new_loc

def neighbors_ptpt_allkeys(adjacencies, loc):
  for new_loc in adjacencies[loc].keys():
    yield new_loc

def neighbors(adjacencies, KEYS, DOORS, state):
  node, found_keys = state
  candidates = adjacencies[node]
  for c in candidates:
    if c in KEYS: 
      new_found_keys = found_keys | {c}
      yield (c, new_found_keys)
    elif c in DOORS and c.lower() in found_keys or c == '@': 
      yield (c, found_keys)

def cost_fn(adjacencies, a, b):
  a_loc = a[0]; b_loc = b[0]
  return adjacencies[a_loc][b_loc]

def one(INPUT):
  G = library.Grid(grid=[list(l) for l in INPUT])
  KEYS = {c: G.detect(c)[0] for c in 'abcdefghijklmnopqrstuvwxyz' if G.detect(c)}
  DOORS = {c.upper(): G.detect(c.upper())[0] for c in 'abcdefghijklmnopqrstuvwxyz' if G.detect(c.upper())}
  start_loc = G.detect('@')[0]
  G.set(start_loc, '1')
  POIS = DOORS | KEYS | {'1': start_loc}

  ## Step 1: Collapse the maze into a graph.
  adjacencies = defaultdict(dict)
  def neighbor_cost(G, loc):
    for new_loc, val in G.neighbors_kv(loc, default='#'):
      if val != '#':
        yield 1, new_loc
  for poi1 in POIS.keys():
    dist, prev, goals = library.dijkstra_lazy(POIS[poi1], partial(neighbor_cost, G), lambda a: G.get(a) in POIS)
    adjacencies[poi1] = {G.get(loc): dist[loc] for loc in goals}

  best_case_adjacencies = defaultdict(dict)

  # Step 2: compute best cases
  for poi1 in POIS.keys():
    for poi2 in POIS.keys():
      path = library.a_star_lazy(poi1, poi2,
                                 lambda x: 0,
                                 partial(neighbors_ptpt_allkeys, adjacencies))
      if poi1 != poi2 and path: 
        best_case_adjacencies[poi1][poi2] = sum([adjacencies[p1[0]][p2[0]] for p1, p2 in zip(path, path[1:])])

  min_steps = {k:min(v.values()) for k, v in best_case_adjacencies.items()}
  def h(min_steps, state):
    ms = [min_steps[k] for k in KEYS.keys() if k not in state[1]]
    return sum(ms) 

  # Step 3: Traverse
  start = ('1', set())
  goal_fn = lambda state: len(state[1]) == len(KEYS)
  path = library.a_star_lazy(start, None, 
                             partial(h, min_steps), 
                             partial(neighbors, adjacencies, KEYS, DOORS), 
                             partial(cost_fn, adjacencies), goal_fn, debug=False)
  cost = sum([adjacencies[p1[0]][p2[0]] for p1, p2 in zip(path, path[1:])])
  return cost

def two(INPUT):
  G = library.Grid(grid=[list(l) for l in INPUT])
  KEYS = {c: G.detect(c)[0] for c in 'abcdefghijklmnopqrstuvwxyz' if G.detect(c)}
  DOORS = {c.upper(): G.detect(c.upper())[0] for c in 'abcdefghijklmnopqrstuvwxyz' if G.detect(c.upper())}
  start_x, start_y = G.detect('@')[0]
  G.set((start_x - 1, start_y - 1), '1')
  G.set((start_x, start_y - 1), '#')
  G.set((start_x + 1, start_y - 1), '2')

  G.set((start_x - 1, start_y), '#')
  G.set((start_x, start_y), '#')
  G.set((start_x + 1, start_y), '#')
  
  G.set((start_x - 1, start_y + 1), '3')
  G.set((start_x, start_y + 1), '#')
  G.set((start_x + 1, start_y + 1), '4')

  adjacencies = defaultdict(dict)
  POIS = DOORS | KEYS | {'1': (start_x - 1, start_y - 1), '2': (start_x + 1, start_y - 1), '3': (start_x - 1, start_y + 1), '4': (start_x + 1, start_y + 1)}

  ## Step 1: Collapse the maze into a graph.
  adjacencies = defaultdict(dict)
  def neighbor_cost_g(G, loc):
    for new_loc, val in G.neighbors_kv(loc, default='#'):
      if val != '#':
        yield 1, new_loc
  for poi1 in POIS.keys():
    dist, prev, goals = library.dijkstra_lazy(POIS[poi1], partial(neighbor_cost_g, G), lambda a: G.get(a) in POIS)
    adjacencies[poi1] = {G.get(loc): dist[loc] for loc in goals}

  quadrants = dict()
  QUAD_KEYS = ['1', '2', '3', '4']
  neighbor_cost = lambda node: [(cost, n) for (n, cost) in adjacencies[node].items()]
  for poi in QUAD_KEYS:
    dist, prev, goals = library.dijkstra_lazy(poi, neighbor_cost)
    quadrants[poi] = dist

  @lru_cache(maxsize=None)
  def reachable_keys(start, havekeys):
    def neigh_keys(adjacencies, havekeys, node):
      return [(adjacencies[node][k], k) for k in adjacencies[node].keys() if k in k in list(KEYS.keys()) + QUAD_KEYS or k.lower() in havekeys]

    dist, prev, goals = library.dijkstra_lazy(start, partial(neigh_keys, adjacencies, havekeys))
    return {k for k in dist.keys() - start if k in list(KEYS.keys()) + QUAD_KEYS and k not in havekeys}, dist

  @lru_cache(maxsize=None)
  def min_cost(state, havekeys):
    # optimal is min(cost(k, keys+k) for k in keys)
    costs = []
    if len(havekeys) == len(KEYS): return (0, [])
    for i, qk in enumerate(QUAD_KEYS):
      reachable, dist = reachable_keys(state[i], havekeys)
      for k in (KEYS.keys() - havekeys) & reachable:
        new_state = state[:i] + (k,) + state[i+1:]
        marginal_cost = dist[k]
        best_cost, best_path = min_cost(new_state, havekeys | {k})
        costs.append((best_cost+marginal_cost, [k]+best_path))
    return min(costs) if costs else (float('inf'), [])
  out = min_cost(('1', '2', '3', '4'), frozenset())
  return out[0]

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "18")
  p.run(one, 0)
  p.run(two, 0)
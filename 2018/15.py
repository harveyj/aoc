#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict, deque
import networkx as nx
import itertools

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

START_HP, START_ATTACK = 200, 3

def book_sort(locs):
  return sorted(locs, key= lambda a: (a[1], a[0]))

def bfs(G, loc, tgt):
  def nxt(G, loc):
    return [(loc, neigh_loc) for (neigh_loc, neigh_val) in G.neighbors_kv(loc) if neigh_val == '.']
  seen = set()
  queue = deque(nxt(loc))
  min_len = -1
  candidates = []
  while queue:
    path = queue.popleft()
    if path in seen: continue
    if candidates and len(path) > min_len: break
    if tgt in G.neighbors(loc):
      candidates.append(path)
      min_len = len(path)
    for n in nxt(G, loc): queue.append((path) + (n,))
  return candidates

def move2(G, loc, enemy_type):
  candidates = bfs(G, loc, enemy_type)
  if not candidates: return None
  first_steps = [path[1] for path in candidates]
  return book_sort(first_steps)[0] if first_steps else None


def move(G, graph, loc, entities, enemy_type):
  if loc not in graph: return None
  enemies = [loc for loc in entities if entities[loc][0] == enemy_type]
  candidates = []
  for e in enemies:
    for e_neigh_loc, e_neigh_val in G.neighbors_kv(e):
      if e_neigh_val == '.' and e_neigh_loc in graph and nx.has_path(graph, loc, e_neigh_loc):
        candidates.extend(nx.all_shortest_paths(graph, loc, e_neigh_loc))
  if not candidates: return None
  min_len = min([len(c) for c in candidates])
  candidates = [c for c in candidates if len(c) == min_len]
  # print('sorted')
  # for c in candidates:
  #   print(len(c), c)
  # print(loc)
  first_steps = [path[1] for path in candidates]
  # print(first_steps)
  return book_sort(first_steps)[0] if first_steps else None

def dump(G, entities):
  print(G)
  for loc in list(book_sort(entities.keys())):
    print(loc, entities[loc])

  def graph(self):
    DG = nx.DiGraph()
    for x in range(self.max_x()):
      for y in range(self.max_y()):
        c = self.get((x, y))
        for pt, val in self.neighbors_kv((x, y), default='#'):
          if c == '.' and val in '.GE':
            DG.add_edge(pt, (x, y))
    return DG


def one(INPUT):
  G = parse_input(INPUT)
  elves = G.detect('E')
  goblins = G.detect('G')
  entities = {loc: ('E',START_HP, START_ATTACK, loc) for loc in elves}
  entities.update({loc: ('G', START_HP, START_ATTACK, loc) for loc in goblins})
  print(f"INITIALLY")

  print(G)
  for i in range(100):
    for loc in list(book_sort(entities.keys())):
      if loc not in entities: continue # we got killed earlier in the turn
      type, hp, attack, _ = entities[loc]
      enemy = 'G' if type == 'E' else 'E'
      neighbor_enemies = [entities[a[0]] for a in G.neighbors_kv(loc) if a[1] == enemy]
      # print(neighbor_enemies, list(G.neighbors_kv(loc)))
      if not neighbor_enemies:
        ## Move
        G.set(loc, 'S')
        connect = G.graph()
        G.set(loc, '.')
        next_loc = move(G, connect, loc, entities, enemy)
        if next_loc:
          del entities[loc]
          entities[next_loc] = (type, hp, attack, next_loc)
          G.set(next_loc, type)
          loc = next_loc
        else:
          G.set(loc, type)
      neighbor_enemies = [entities[a[0]] for a in G.neighbors_kv(loc) if a[1] == enemy]
      ## Attack
      if neighbor_enemies:
        min_hp = min([e[1] for e in neighbor_enemies])
        neigh_loc = book_sort([ne[3] for ne in neighbor_enemies if ne[1] == min_hp])[0]
        _, neigh_hp, neigh_attack, neigh_loc = entities[neigh_loc]
        neigh_hp -= attack
        if neigh_hp > 0:
          entities[neigh_loc] = (enemy, neigh_hp, neigh_attack, neigh_loc)
        else: 
          del entities[neigh_loc]
          G.set(neigh_loc, '.')
          if enemy not in [e[0] for e in entities.values()]:
            dump(G, entities)
            return i+1, sum([e[1] for e in entities.values()])
      else:
        print(f'no enemies {loc, type}')

    print(f'ROUND {i+1}')
    dump(G, entities)
    print()
    # input()

  return 0

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out


  # G = library.Grid(raw='\n'.join(INPUT))
  # for x in range(G.max_x()):
  #   for y in range(G.max_y()):
  #     c = G.get((x, y))

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "15")
  print(p.run(one, 0))
  print(p.run(two, 0))
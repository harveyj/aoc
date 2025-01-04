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

def bfs2(G, start_loc, tgt):
  def nxt(G, loc):
    return [neigh_loc for (neigh_loc, neigh_val) in G.neighbors_kv(loc) if neigh_val == '.']
  seen = set()
  queue = deque([(a,) for a in nxt(G, start_loc)])
  min_len = 10000000
  candidates = []
  while queue:
    path = queue.popleft(); loc = path[-1]
    seen.add(loc)
    if candidates and len(path) > min_len: break
    if tgt in G.neighbors(loc):
      candidates.append(path)
      min_len = len(path)
    for n in nxt(G, loc): 
      if n not in seen: queue.append((path) + (n,))
    # print(queue)
  return candidates

def bfs(G, start_loc, tgt):
  # ensure neighbors are traversed in book order. cool if it works...
  G.NEIGHBORS = [(0, -1), (-1, 0), (1, 0), (0, 1)]
  def nxt(G, loc):
    return [neigh_loc for (neigh_loc, neigh_val) in G.neighbors_kv(loc) if neigh_val == '.']
  seen = set()
  queue = deque([(a,) for a in nxt(G, start_loc)])
  while queue:
    path = queue.popleft(); loc = path[-1]
    if loc in seen: continue
    seen.add(loc)
    if tgt in G.neighbors(loc):
      return path
    for n in nxt(G, loc): 
      if n not in seen: queue.append((path) + (n,))


def move(G, loc, enemy_type):
  path = bfs(G, loc, enemy_type)
  return path[0] if path else None

def dump(G, entities):
  print(G)
  for loc in list(book_sort(entities.keys())):
    print(loc, entities[loc])

def one(INPUT, two=False, ATTACK_ELF=3):
  G = parse_input(INPUT)
  elves = G.detect('E')
  goblins = G.detect('G')
  entities = {loc: ('E',START_HP, ATTACK_ELF, loc) for loc in elves}
  entities.update({loc: ('G', START_HP, 3, loc) for loc in goblins})
  # print(f"INITIALLY")
  # print(G)
  for i in range(100):
    for loc in list(book_sort(entities.keys())):
      if loc not in entities: continue # we got killed earlier in the turn
      type, hp, attack, _ = entities[loc]
      enemy = 'G' if type == 'E' else 'E'
      neighbor_enemies = [entities[a[0]] for a in G.neighbors_kv(loc) if a[1] == enemy]
      # print(neighbor_enemies, list(G.neighbors_kv(loc)))
      if not neighbor_enemies:
        ## Move
        G.set(loc, '.')
        next_loc = move(G, loc, enemy)
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
          if two and enemy == 'E': return -1
          del entities[neigh_loc]
          G.set(neigh_loc, '.')
          if enemy not in [e[0] for e in entities.values()]:
            rem_hp = sum([e[1] for e in entities.values()])
            return i*rem_hp

def two(INPUT):
  for i in range(3, 20):
    res = one(INPUT, two=True, ATTACK_ELF=i)
    if res != -1: return res

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "15")
  print(p.run(one, 0))
  print(p.run(two, 0))
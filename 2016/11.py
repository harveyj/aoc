#!/usr/bin/env python3
import puzzle
import networkx as nx
import itertools

CHIPS = set(['Pr-C', 'Co-C', 'Cu-C', 'Ru-C', 'Pu-C', 'El-C', 'Di-C'])
GENS = set(['Pr-G', 'Co-G', 'Cu-G', 'Ru-G', 'Pu-G', 'El-G', 'Di-G'])
CHIP_TO_GEN = {'Pr-C': 'Pr-G', 
               'Co-C': 'Co-G', 
               'Cu-C': 'Cu-G', 
               'Ru-C': 'Ru-G', 
               'Pu-C': 'Pu-G', 
               'El-C': 'El-G', 
               'Di-C': 'Di-G', 
               }

# Test input
# CHIPS = set(['H-C', 'Li-C',])
# GENS = set(['H-G', 'Li-G'])
# CHIP_TO_GEN = {'H-C': 'H-G', 
#                'Li-C': 'Li-G', 
#                }

def legal(state):
  floors, elev_id = state
  for id, fl in enumerate(floors):
    # print(fl)
    gens = fl.intersection(GENS)
    chips = fl.intersection(CHIPS)
    if len(gens) != 0:
      for c in chips:
        if CHIP_TO_GEN[c] not in gens:
          return False
  return True

def freeze(floors):
  return tuple(frozenset(s) for s in floors)

def run(state, total=10):
  seen = set()
  graph = nx.DiGraph()
  graph.add_node('START')
  graph.add_node('END')
  graph.add_edge('START', (freeze(state[0]), state[1]))
  pending = [state]
  while pending:
    if len(pending) % 100 == 0:
      print(len(pending)) 
    state = pending.pop()
    floors, elev = state
    if state in seen: continue
    graph.add_node(state)
    seen.add(state)
    if len(floors[3]) == total:
      graph.add_edge(state, 'END')
    moves = []
    if elev > 0: moves.append((elev, elev - 1))
    if elev < 3: moves.append((elev, elev + 1))
    for elev, new_elev in moves:
      for a in floors[elev]:
        new_floors = list(set(f) for f in floors)
        new_floors[elev].discard(a)
        new_floors[new_elev].add(a)
        new_state = new_floors, new_elev
        new_state_immutable = freeze(new_floors), new_elev
        if legal(new_state):
          graph.add_edge(state, new_state_immutable)
          if not new_state_immutable in seen:
            pending.append(new_state_immutable)
      for a, b in itertools.combinations(floors[elev], 2):
        new_floors = list(set(f) for f in floors)
        new_floors[elev].discard(a)
        new_floors[elev].discard(b)
        new_floors[new_elev].add(a)
        new_floors[new_elev].add(b)
        new_state = new_floors, new_elev
        new_state_immutable = freeze(new_floors), new_elev
        if legal(new_state):
          graph.add_edge(state, new_state_immutable)
          if not new_state_immutable in seen:
            pending.append(new_state_immutable)

  dp = nx.dijkstra_path(graph, "START", "END")
  for item in dp[1:-1]:
    # print(item)
    state = []
    for label in ['Pr-G', 'Pr-C', 'Co-G', 'Co-C', 'Cu-G', 'Cu-C', 'Ru-G', 'Ru-C', 'Pu-G', 'Pu-C', 'E']:
      for i in range(4):
        if label in item[0][i]:
          state.append(i)
    state.append(item[1])
    print(state)

  return len(dp) - 3

def one(INPUT):
  # state = (set(['H-C', 'Li-C']), set(['H-G']), set(['Li-G']), set()), 0
  state = freeze((set(['Pr-G', 'Pr-C']), 
          set(['Co-G', 'Cu-G', 'Ru-G', 'Pu-G']),
          set(['Co-C', 'Cu-C', 'Ru-C', 'Pu-C']),
          set())), 0
  return run(state)


def legal2(state):
  # print("checking", state)
  c_idx = range(1, len(state)-1, 2)
  g_levels = set([state[i] for i in range(0, len(state)-1, 2)])
  # print(state, 'gl', g_levels)
  for c_i in c_idx:
    if state[c_i] in g_levels and not state[c_i-1] == state[c_i]:
      # print('bail', c_i)
      return False
  return True

def run2(state, labels=None):
  seen = set()
  graph = nx.DiGraph()
  graph.add_node('START')
  graph.add_node('END')
  graph.add_edge('START', state)
  pending = [state]
  while pending:
    # if len(pending) > 5:
    #   print(pending)
    #   return
    # if len(pending) % 100 == 0:
    #   print(len(pending), pending[-1])
    state = pending.pop()
    elev = state[-1]
    if state in seen: continue
    graph.add_node(state)
    seen.add(state)
    if state[:-1].count(3) == len(state) - 1:
      print('FOUND END')
      graph.add_edge(state, 'END')
    moves = []
    if elev > 0: moves.append((elev, elev - 1))
    if elev < 3: moves.append((elev, elev + 1))
    for elev, new_elev in moves:
      legal_idx = [x for x in range(len(state)-1) if state[x] == elev]
      for a in legal_idx:
        new_state = [x for x in state]
        new_state[a] = new_elev
        new_state[-1] = new_elev
        new_state = tuple(new_state)
        if legal2(new_state):
          graph.add_edge(state, new_state)
          if not new_state in seen:
            pending.append(new_state)
      for a, b in itertools.combinations(legal_idx, 2):
        new_state = [x for x in state]
        new_state[a] = new_elev
        new_state[b] = new_elev
        new_state[-1] = new_elev
        new_state = tuple(new_state)
        if legal2(new_state):
          graph.add_edge(state, new_state)
          if not new_state in seen:
            pending.append(new_state)

  # print(f'seen, {seen}')
  print(graph)
  check_path = [[0, 0, 1, 2, 1, 2, 1, 2, 1, 2, 0],
[1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1],
[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2],
[1, 3, 1, 2, 1, 2, 1, 3, 1, 2, 3],
[1, 2, 1, 2, 1, 2, 1, 3, 1, 2, 2],
[1, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1],
[2, 2, 1, 1, 2, 2, 1, 3, 1, 1, 2],
[2, 3, 1, 1, 2, 3, 1, 3, 1, 1, 3],
[2, 2, 1, 1, 2, 3, 1, 3, 1, 1, 2],
[2, 2, 1, 1, 1, 3, 1, 3, 1, 1, 1],
[2, 2, 1, 1, 2, 3, 2, 3, 1, 1, 2],
[2, 2, 1, 1, 3, 3, 3, 3, 1, 1, 3],
[2, 2, 1, 1, 2, 2, 3, 3, 1, 1, 2],
[3, 2, 1, 1, 3, 2, 3, 3, 1, 1, 3],
[3, 2, 1, 1, 3, 2, 3, 2, 1, 1, 2],
[3, 3, 1, 1, 3, 3, 3, 2, 1, 1, 3],
[3, 3, 1, 1, 3, 3, 2, 2, 1, 1, 2],
[3, 3, 1, 1, 3, 3, 1, 2, 1, 1, 1],
[3, 3, 1, 2, 3, 3, 1, 2, 1, 2, 2],
[3, 3, 1, 1, 3, 3, 1, 2, 1, 2, 1],
[3, 3, 1, 1, 3, 3, 2, 2, 2, 2, 2],
[3, 3, 1, 1, 3, 3, 3, 2, 3, 2, 3],
[3, 2, 1, 1, 3, 3, 3, 2, 3, 2, 2],
[3, 3, 1, 1, 3, 3, 3, 2, 3, 3, 3],
[3, 3, 1, 1, 3, 3, 2, 2, 3, 3, 2],
[3, 3, 1, 1, 3, 3, 1, 2, 3, 3, 1],
[3, 3, 2, 1, 3, 3, 2, 2, 3, 3, 2],
[3, 3, 1, 1, 3, 3, 2, 2, 3, 3, 1],
[3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2],
[3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3],
[3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 2],
[3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3],
[3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]

  # print(list(graph.nodes.keys())[2])

  # for edge in zip(check_path, check_path[1:]):
    
  #   if not graph.has_node(edge[0]):
  #     print('ERROR', tuple(edge[0]))
  #     return
  #   if not graph.has_edge(tuple(edge[0]), tuple(edge[1])):
  #     print(f'ERROR: missing edge {edge}')

  dp = nx.dijkstra_path(graph, "START", "END")
  # if labels:
  #   for node in dp[1:-1]:
  #     # print(len(node))
  #     print([(labels[i], node[i]) for i in range(len(node))])

  return len(dp) - 3 # START, END, and fencepost off by one


def oneagain(INPUT):
  # Evens are G
  labels = ['Pr-G', 'Pr-C', 'Co-G', 'Co-C', 'Cu-G', 'Cu-C', 'Ru-G', 'Ru-C', 'Pu-G', 'Pu-C', 'E']
  state = list(0 for i in range(11))
  state[0] = 0; state[1] = 0
  state[2] = 1; state[3] = 2
  state[4] = 1; state[5] = 2
  state[6] = 1; state[7] = 2
  state[8] = 1; state[9] = 2  
  state[-1] = 0
  # print(legal2(state))
  return run2(tuple(state), labels)

def test(INPUT):
  # Evens are G
  labels = ['HG', 'HM', 'LG', 'LM', 'E']
  state = list(0 for i in range(5))
  state[0] = 1; state[1] = 0
  state[2] = 2; state[3] = 0
  state[-1] = 0

  # print(legal2(state))
  return run2(tuple(state), labels)

def testtwo(INPUT):
  # Evens are G
  labels = ['Pr-G', 'Pr-C', 'Co-G', 'Co-C', 'Cu-G', 'Cu-C', 'Ru-G', 'Ru-C', 'Pu-G', 'Pu-C', 'E']
  # state = list(0 for i in range(9))
  # state[0] = 1; state[1] = 2
  # state[2] = 1; state[3] = 2
  # state[4] = 1; state[5] = 2
  # state[6] = 1; state[7] = 2
  # state[-1] = 0
  # # print(legal2(state))
  # print('no on bottom', run2(tuple(state), labels))

  state = list(0 for i in range(11))
  state[0] = 0; state[1] = 0
  state[2] = 1; state[3] = 2
  state[4] = 1; state[5] = 2
  state[6] = 1; state[7] = 2
  state[8] = 1; state[9] = 2  
  state[-1] = 0
  # print(legal2(state))
  print('pair on bottom', run2(tuple(state), labels))

  state = list(0 for i in range(13))
  state[0] = 0; state[1] = 0
  state[2] = 1; state[3] = 2
  state[4] = 1; state[5] = 2
  state[6] = 1; state[7] = 2
  state[8] = 1; state[9] = 2  
  state[9] = 0; state[10] = 0

  state[-1] = 0
  # print(legal2(state))
  print('two pair on bottom', run2(tuple(state), labels))

# TODO don't remember how I did this one, I think i extrapolated how many extra steps each new pair would generate.
def two(INPUT):
  # Evens are G
  state = list(0 for i in range(15))
  state[6] = 1; state[8] = 1; state[10] = 1; state[12] = 1
  state[7] = 2; state[9] = 2; state[11] = 2; state[13] = 2
  state[14] = 0
  # print(legal2(state))
  return run2(tuple(state))

p = puzzle.Puzzle("2016", "11")
# p.run(one, 0)
p.run(oneagain, 0)
# p.run(two, 0)

# p.run(testtwo, 0)

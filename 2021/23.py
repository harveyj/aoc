import itertools
import networkx
import copy
import collections
import puzzle

def one(INPUT):
  state = {}
  for y, l in enumerate(INPUT):
    for x, c in enumerate(l):
      if c not in '. #':
        state[c] = (x, y)
  start_state = repr(state)

  # graph lowest cost path
  # vertex state = (a_loc, A_loc, b_loc, B_loc, c_loc, C_loc, d_loc, D_loc)
  # edges = all possible new states
  # each amphipod in a pod can move to 1, 2, 4, 6, 8, 10, 11 or its home
  # each amphipod not in its home can move to its home
  # edge cost = which one you move
  HOMES = {'a': 3, 'A': 3, 'b': 5, 'B': 5, 'c': 7, 'C': 7, 'd': 9, 'D': 9}
  COSTS = {'a': 1, 'A': 1, 'b': 10, 'B': 10, 'c': 100, 'C': 100, 'd': 1000, 'D': 1000}
  LEGAL = [1, 2, 4, 6, 8, 10, 11]
  end = "{'c': (7, 2), 'A': (3, 2), 'b': (5, 2), 'd': (9, 2), 'a': (3, 3), 'B': (5, 3), 'C': (7, 3), 'D': (9, 3)}"
  def is_end(state):
    # print(state)
    return len([c for (c, (x,y)) in state.items() if x == HOMES[c]]) == 8

  def all_edges(state):
    moves = []
    if state == 'END': return []
    if is_end(state):
      print('found end', state)
      return [(state, 'END', 0)]
    tops = [(c, x) for (c, (x, y)) in state.items() if y == 1]
    tops_rev = {x:c for (c, (x, y)) in state.items() if y == 1}
    twos = [(c, x) for (c, (x, y)) in state.items() if y == 2]
    twos_rev = {x:c for (c, (x, y)) in state.items() if y == 2}
    threes = [(c, x) for (c, (x, y)) in state.items() if y == 3]
    threes_rev = {x:c for (c, (x, y)) in state.items() if y == 3}

    for c, x in tops:
      blockers = [c2 for c2, x in twos if x == HOMES[c] and c2.upper() != c.upper()] + [c2 for c2, x in threes if x == HOMES[c] and c2.upper() != c.upper()]
      blockers += [c2 for c2, x2 in tops if HOMES[c] < x2 < x or x < x2 < HOMES[c] ]
      if not blockers:
        new_state = copy.copy(state)
        new_state[c] = (HOMES[c], 2 if threes_rev.get(HOMES[c], None) else 3)
        # print(c, x, HOMES[c], new_state[c])
        cost = COSTS[c] * (abs(x - HOMES[c])+new_state[c][0] - 1)

        # print('move', c , 'to', HOMES[c], "cost", cost)
        moves.append((state, new_state, cost))
    for c, x in twos:
      top_x = [0] + sorted(tops_rev.keys()) + [12]
      for x1, x2 in zip(top_x, top_x[1:]):
        if x1 < x < x2: 
          for n_x in [l for l in LEGAL if x1 < l < x2]:
            new_state = copy.copy(state)
            new_state[c] = (n_x, 1)
            cost = COSTS[c] * (abs(n_x - x)+1)
            # print('move', c , 'to', n_x, "cost", cost)
            moves.append((state, new_state, cost))
    for c, x in threes:
      if x in twos_rev: continue
      if x == HOMES[c]: continue
      top_x = [0] + sorted(tops_rev.keys()) + [12]
      for x1, x2 in zip(top_x, top_x[1:]):
        if x1 < x < x2: 
          for n_x in [l for l in LEGAL if x1 < l < x2]:
            new_state = copy.copy(state)
            new_state[c] = (n_x, 1)
            cost = COSTS[c] * (abs(n_x - x)+2)
            # print('move', c , 'to', n_x, "cost", cost)
            moves.append((state, new_state, cost))
    return moves

  DG = networkx.DiGraph()
  q = collections.deque([state])
  seen = set()
  while q:
    state = q.pop()
    # print(state)
    # print('.', end='')
    if repr(state) in seen: continue
    seen.add(repr(state))
    ae = all_edges(state)
    graph_ae = [(repr(os), repr(ns), cost) for os, ns, cost in ae]
    # print(graph_ae)
    DG.add_weighted_edges_from(graph_ae)
    q.extend([new_state for _, new_state, _2 in ae])
  print(is_end({'a': (3,2), 'A': (3,3), 'b': (5,2), 'B': (5,3), 'c': (7,2), 'C': (7,3), 'd': (9,2), 'D': (9,3)}))
  # print(DG.edges(end))
  # print(DG.has_node(end))
  sp = networkx.shortest_path(DG, start_state, "'END'", weight="weight")
  cost = 0
  for s1, s2 in zip(sp, sp[1:]):
    s1, s2 = eval(s1), eval(s2)
    diff = [(k, s1[k], s2[k]) for k in s1 if s2 != "END" and s1[k] != s2[k]]
    if diff:
      diff = diff[0]
      cost += COSTS[diff[0]] * (abs(diff[1][0] - diff[2][0])+abs(diff[1][1] - diff[2][1]))
  # print(networkx.shortest_path_length(DG, start_state, "'END'", weight="weight"))
  print(cost)

def two(INPUT):
  lines = INPUT

  state = {}
  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      if c not in '. #':
        state[(c, str(x) + str(y))] = (x, y)
  start_state = repr(state)

  COLS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
  COSTS = {'a': 1, 'A': 1, 'b': 10, 'B': 10, 'c': 100, 'C': 100, 'd': 1000, 'D': 1000}
  LEGAL = [1, 2, 4, 6, 8, 10, 11]

  def is_end(state):
    # print([c for ((c, uid), (x,y)) in state.items() if x == COLS[c]])
    return len([c for ((c, uid), (x,y)) in state.items() if x == COLS[c]]) == len(state)

  def all_edges(state):
    moves = []
    if state == 'END': return []
    if is_end(state):
      # print('found end', state)
      return [(state, 'END', 0)]
    tops = [((c, uid), x) for ((c, uid), (x, y)) in state.items() if y == 1]
    top_occupied = [x for (_, (x, y)) in state.items() if y == 1]
    cols = {x: [(loc[1], key) for (key, loc) in state.items() if loc[0] == x] for x in COLS.values()}
    for (c, uid), x in tops:
      if [x2 for x2 in top_occupied if x <  x2 < COLS[c] or x > x2 > COLS[c]]: continue
      tgt_col = [(y, c2) for (y, c2) in cols.get(COLS[c], [])]
      blockers = [c2 for (y, (c2, uid)) in tgt_col if c2 != c]
      if not blockers:
        top_y, _ = min(tgt_col) if tgt_col else ((2 + len(state)//4), None)
        new_state = copy.copy(state)
        new_state[(c, uid)] = (COLS[c], top_y -1)
        cost = COSTS[c] * (abs(x - COLS[c])+top_y -1)
        # print('move', c , 'to', COLS[c], "cost", cost)
        moves.append((state, new_state, cost))

    for x in cols:
      # skip this if empty
      if not cols[x]: continue
      correct = [c for y, (c, uid) in cols[x] if x == COLS[c]]
      # skip this if there are only correct values 
      if len(correct) == len(cols[x]): continue
      top_y, (top_c, top_uid) = min(cols[x])

      top_x = [0] + sorted([x for (c, x) in tops]) + [12]
      for x1, x2 in zip(top_x, top_x[1:]):
        if x1 < x < x2: 
          for n_x in [l for l in LEGAL if x1 < l < x2]:
            new_state = copy.copy(state)
            new_state[(top_c, top_uid)] = (n_x, 1)
            cost = COSTS[top_c] * (abs(n_x - x) + (top_y - 1))
            # print('move', top_c , 'to', n_x, "cost", cost)
            moves.append((state, new_state, cost))
    return moves

  DG = networkx.DiGraph()
  q = collections.deque([state])
  seen = set()
  while q:
    state = q.pop()
    if repr(state) in seen: continue
    seen.add(repr(state))
    ae = all_edges(state)
    graph_ae = [(repr(orig_state), repr(new_state), cost) for orig_state, new_state, cost in ae]
    # print("graph_ae", graph_ae)
    # print('ae', ae)
    DG.add_weighted_edges_from(graph_ae)
    q.extend([new_state for _, new_state, _2 in ae])
  sp = networkx.shortest_path(DG, start_state, "'END'", weight="weight")
  cost = 0
  for s1, s2 in zip(sp, sp[1:]):
    s1, s2 = eval(s1), eval(s2)
    diff = [(k, s1[k], s2[k]) for k in s1 if s2 != "END" and s1[k] != s2[k]]
    print(diff)
    if diff:
      diff = diff[0]
      cost += COSTS[diff[0][0]] * (abs(diff[1][0] - diff[2][0])+abs(diff[1][1] - diff[2][1]))
  print(cost)

p = puzzle.Puzzle("2021", "23")
p.run(one, 0)
p.run(two, 0)


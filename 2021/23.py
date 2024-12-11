import itertools
import networkx
import copy
import collections
import puzzle

def run(INPUT):
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

p = puzzle.Puzzle("23")
# p.run(run, 0)
p.run(run, 3)


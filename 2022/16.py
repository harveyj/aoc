#!/usr/bin/env python3
from collections import deque
import puzzle
import re
import networkx as nx
from collections import namedtuple

State = namedtuple("State", "where when opens")

def parse(INPUT):
  ret = []
  for l in INPUT.split('\n'):
    match = re.match("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((\w+,? ?)+)", l)
    name = match.group(1)
    rate = int(match.group(2))
    outs = list(re.findall('\w+', match.group(3)))
    ret.append([name, rate, outs])
  return ret

def next_states(state, dists, flows, flows_nz_nodes):
  if state.when <= 0: return []
  ret = []
  for node in flows_nz_nodes:
    next_when = state.when - dists[state.where][0][node]
    if next_when < 0 or state.where == node: continue
    ns = State(node, next_when, state.opens)
    ret.append([ns, 0])
    # print(state, ns)

  if state.where not in state.opens:
    ns = State(state.where, state.when-1, tuple(sorted(state.opens +(state.where,))))
    ret.append((ns, (state.when-1)* flows[state.where]))
  return ret

def one(INPUT):
  nodes = parse(INPUT)
  flows = {name:rate for name, rate, _ in nodes}
  flows_nz = {name:rate for name, rate, _ in nodes if rate > 0}
  flows_nz_nodes = list(flows_nz.keys())
  print(flows)
  G = nx.Graph()
  for name, _, outs in nodes:
    G.add_node(name)
    for o in outs:
      G.add_edge(name, o)
  dists = dict(nx.all_pairs_dijkstra(G))

  SG = nx.DiGraph()
  start_state = State(where='AA', when=30, opens=())
  states = deque([start_state])
  seen = set()
  SG.add_node(start_state)

  while states:
    state = states.popleft()
    if state in seen: continue
    seen.add(state)
    for (ns, weight) in next_states(state, dists, flows, flows_nz_nodes):
      SG.add_edge(state, ns, weight=weight)
      if not ns in seen:
        states.appendleft(ns)

  lp = nx.dag_longest_path(SG, weight="weight")
  for node in lp: print(node)
  lpw = nx.dag_longest_path_length(SG, weight="weight")
  return lpw


  # can you dynamic program this?
  # optimal thing to do at time 1 given loc1, loc2, opens
  # you can but the number of locations is 54 = 2**54
  # BUT non-zero flows only = 15
  # roughly 100M states per time t
  # the issue is that almost all of your end states are impossible

  # is it just the order in which the nodes are opened?
  # 15! = 1.3T

  # is it beam search?
  # states = [] (width N)
  # foreach next state:
  #   generate all possible next states
  #   rank them by heuristic

BeamState = State = namedtuple("State", "where_p where_e banked opens")
ScoredBeamState = State = namedtuple("State", "beam score")

def two(INPUT):
  DURATION = 26
  WIDTH = 1000
  nodes = parse(INPUT)
  flows = {name:rate for name, rate, _ in nodes}

  G = nx.Graph()
  for name, _, outs in nodes:
    G.add_node(name)
    for o in outs:
      G.add_edge(name, o)
  
  def score(beam_state):
    return beam_state.banked

  start_state = BeamState(where_p='AA', where_e = 'AA', banked=0, opens=())
  states = deque([start_state])

  for i in range(DURATION):
    new_states = []
    for state in states:
      new_person_states = []
      new_elephant_states = []
      for e in G[state.where_p]:
       new_person_states.append((e, None))
      for e in G[state.where_e]:
       new_elephant_states.append((e, None))
      if state.where_p not in state.opens and flows[state.where_p] != 0:
        new_person_states.append((state.where_p, state.where_p))
      if state.where_e not in state.opens  and flows[state.where_e] != 0:
        new_elephant_states.append((state.where_e, state.where_e))

      for nps in new_person_states:
        for nes in new_elephant_states:
          where_p, p_open = nps
          where_e, e_open = nes
          if p_open and p_open == e_open: continue

          banked = state.banked + (flows[p_open] * (DURATION - i - 1) if p_open else 0) + (flows[e_open]* (DURATION - i - 1) if e_open else 0)
          opens = state.opens
          if p_open: opens += (p_open,)
          if e_open: opens += (e_open,)
          new_states.append(BeamState(where_p=where_p, where_e=where_e, banked=banked, opens=opens))
      new_states = sorted(new_states, key=score)
      new_states = new_states[-WIDTH:]
      states = new_states
  return states[-1].banked

p = puzzle.Puzzle("16")
# p.run(one, 0)
p.run(two, 0)

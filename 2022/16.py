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


def two(INPUT):
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

p = puzzle.Puzzle("16")
p.run(one, 0)
p.run(two, 0)

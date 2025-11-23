#!/usr/bin/env python3
import puzzle, networkx as nx
from collections import deque, defaultdict

def parse_input(INPUT):
  def parse_line(l):
    src, outs = l.split('->')
    src = src.strip()
    outs = [o.strip() for o in outs.split(',')]
    code = ''
    if src == 'broadcaster':
      code = 'broadcaster'
    if src[0] in ['%', '&']:
      code = src[0]
      src = src[1:]
    return src, code, outs
  return [parse_line(l) for l in INPUT]

def out_edges(G, src):
  return [dst for _, dst in G.edges(src)]

def create_network(instrs):
  G = nx.DiGraph()
  state = {}
  for (src, code, outs) in instrs:
    G.add_node(src, code=code)
    for o in outs:
      G.add_edge(src, o)
  for (src, code, outs) in instrs:
    for o in outs:
      if not G.nodes[o]:
        state[o] = 0
        G.add_node(o, code=None)
    incoming_nodes = [u for u, v in G.edges() if v == src]
    if code == '%':
      state[src] = False
    elif code == '&': 
      state[src] = {node: 'low' for node in incoming_nodes}
  return G, state

def simulate(G, state, n):
  def handle(G, state, signal, src):
    code = G.nodes[src]['code']
    tgts = out_edges(G, src)
    out_signal = signal
    if code == '%':
      if signal == 'high': return []
      out_signal = "low" if state[src] else 'high'
      state[src] = not state[src]
    elif code == '&':
      out_signal = 'high'
      if len(state[src]) == list(state[src].values()).count('high'):
        out_signal = 'low'

    # update any conjunction targets
    for tgt in tgts:
      if type(state[tgt]) == type({}):
        state[tgt][src] = out_signal
    # broadcaster just passes signal to all tgts, so do nothing
    return [(out_signal, dst) for dst in tgts]

  out_h = 0; out_l = 0 
  all_pulses = defaultdict(list)
  for i in range(n):
    out_l += 1 # account for initial 'button'
    q = deque(handle(G, state, 'low', 'broadcaster'))
    while q:
      pulse, tgt = q.popleft()
      all_pulses[(tgt, pulse)].append(i)
      q.extend(handle(G, state, pulse, tgt))
      if pulse == 'high': out_h += 1
      if pulse == 'low': out_l += 1
  return out_h, out_l, all_pulses, state

def one(INPUT):
  instrs = parse_input(INPUT)
  G, state = create_network(instrs)
  out_h, out_l, _, _ = simulate(G, state, 1000)
  return (out_h * out_l) 

# A teeny bit by inspection but I think this is pretty cool. 
def two(INPUT):
  instrs = parse_input(INPUT)
  G, state = create_network(instrs)
  H = G.reverse()
  second_tier = []
  for n in list(H.neighbors('rx')):
    second_tier = list(H.neighbors(n))
  out_h, out_l, all_pulses, state = simulate(G, state, 10000)
  ans = 1
  for key in second_tier:
    ans *= all_pulses[(key, 'low')][0] + 1
  return ans

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "20")

  p.run(one, 0) 
  p.run(two, 0) 

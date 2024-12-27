#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx
import collections

Gate = collections.namedtuple('Gate', ['op', 'in0', 'in1', 'out'])

def process_wire(id, val):
  return str(id).zfill(2), val

def parse_input(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  x_wires_raw = chunks[0].split('y00')[0].strip().split('\n')
  y_wires_raw = ('y00'+chunks[0].split('y00')[1]).strip().split('\n')  # sue me
  x_wires = [process_wire(*library.ints(wire)) for wire in x_wires_raw]
  y_wires = [process_wire(*library.ints(wire)) for wire in y_wires_raw]
  gates_raw = chunks[1].split('\n')
  gates_split = [gate_raw.split() for gate_raw in gates_raw]
  gates = [Gate(op, in0, in1, out) for (in0, op, in1, _, out) in gates_split]
  return x_wires, y_wires, gates

def apply(op, vals, in0, in1):
  wires = vals[in0], vals[in1]
  if op == 'AND':
    return 1 if wires == (1, 1) else 0
  elif op == 'OR':
    return 1 if 1 in wires else 0
  elif op == 'XOR':
    return 1 if wires in [(1,0), (0,1)] else 0

def sim(x_wires, y_wires, gates):
  vals = defaultdict(int)
  all = set()
  for g in gates:
    all.add(g.out)
  for xw in x_wires:
    vals[f'x{xw[0]}'] = xw[1]
    all.add(f'x{xw[0]}')
  for yw in y_wires:
    vals[f'y{yw[0]}'] = yw[1]
    all.add(f'y{yw[0]}')
  while len(vals) != len(all):
    for g in gates:
      if g.in0 in vals and g.in1 in vals:
        vals[g.out] = apply(g.op, vals, g.in0, g.in1)
  out = 0; i = 0
  zvals = ({key: value for (key, value) in vals.items() if key[0] == 'z'})
  for z_key, z_value in zvals.items():
    if z_value == 1:
      out += 2**int(z_key[1:])
    i += 1
  return out

def one(INPUT):
  x_wires, y_wires, gates = parse_input(INPUT)
  return sim(x_wires, y_wires, gates)

def bits(inval):
  return list(map(int, bin(inval)[2:].zfill(50)))[::-1]

def op(G, out):
  edges = G.in_edges(out)
  if len(edges) == 0:
    return None
  u, v = list(edges)[0]
  return G.get_edge_data(u, v)['op']

def swap_gates(gates, codes_translate):
  new_gates = list()
  for g in gates:
    new_gate = g
    if g.out in codes_translate:
      new_gate = Gate(g.op, g.in0, g.in1, codes_translate[g.out])
    new_gates.append(new_gate)
  return new_gates

def check(a, b, gates):
  xw = [(str(i).zfill(2), x) for i, x in enumerate(bits(a))]
  yw = [(str(i).zfill(2), y) for i, y in enumerate(bits(b))]
  return sim(xw, yw, gates)

def two(INPUT):
  _, _, gates = parse_input(INPUT)
  DG = nx.DiGraph()
  gate_swaps = {
    'gsd': 'z26', 'z26': 'gsd',
    'kth': 'z12', 'z12': 'kth', 
    'z32': 'tbt', 'tbt': 'z32',
    'vpm': 'qnf', 'qnf': 'vpm'
  }
  gates = swap_gates(gates, gate_swaps)
  gate_lookup = {(g.in0, g.in1, g.op): g.out for g in gates}
  gate_lookup.update({(g.in1, g.in0, g.op): g.out for g in gates})

  for g in gates:
    DG.add_edge(g.in0, g.out, op=g.op)
    DG.add_edge(g.in1, g.out, op=g.op)

  prev_carry = gate_lookup[('x00', 'y00', 'AND')]
  for id in range(1, 45):
    str_id = str(id).zfill(2)
    inputs_xor = gate_lookup[('x'+str_id, 'y'+str_id, 'XOR')]
    inputs_and = gate_lookup[('x'+str_id, 'y'+str_id, 'AND')]
    out = gate_lookup[(prev_carry, inputs_xor, 'XOR')]
    carry_and = gate_lookup[(prev_carry, inputs_xor, 'AND')]
    carry = gate_lookup[(carry_and, inputs_and, 'OR')]
    prev_carry = carry

  return '-'.join(sorted(gate_swaps.keys()))
if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "24")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')

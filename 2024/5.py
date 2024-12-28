#!/usr/bin/env python3
import puzzle
import networkx as nx

def segment_packets(rules, packets):
  good = []
  illegal_packets = []
  for packet in packets:
    vals = packet.split(',')
    forbidden = set()
    for a, b in rules:
      if a in vals:
        forbidden.add((b, a))
    illegal_vals = [(v, v2) for v, v2 in zip(vals, vals[1:]) if (v, v2) in forbidden]

    if len(illegal_vals) == 0: 
      good.append(int(vals[len(vals)//2]))
    else: 
      illegal_packets.append(packet)
  return good, illegal_packets

def one(INPUT):
  raw = '\n'.join(INPUT)
  rules, packets = raw.split('\n\n')
  rules = rules.split('\n')
  rules = [r.split('|') for r in rules]
  packets = packets.split('\n')
  good, _ = segment_packets(rules, packets)
  return sum(good)

def two(INPUT):
  raw = '\n'.join(INPUT)
  rules, packets = raw.split('\n\n')
  rules = rules.split('\n')
  rules = [r.split('|') for r in rules]
  packets = packets.split('\n')
  _, illegal_packets = segment_packets(rules, packets)
  out = []
  for packet in illegal_packets:
    vals = packet.split(',')
    G = nx.DiGraph()
    for r in [r for r in rules if r[0] in vals and r[1] in vals]:
      G.add_edge(*r)
    sorted_packet = list(map(int, nx.topological_sort(G)))
    out.append(int(sorted_packet[len(sorted_packet)//2]))
  return sum(out)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "5")

  p.run(one, 0)
  p.run(two, 0)

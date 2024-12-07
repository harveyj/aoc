#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  pat_value = re.compile('value (\d+) goes to bot (\d+)')
  pat_bot = re.compile('bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')
  for l in INPUT:
    value = re.match(pat_value, l)
    bot = re.match(pat_bot, l)
    if value:
      yield ('value', value.groups())
    elif bot:
      yield ('bot', bot.groups())


def one(INPUT, DEBUG=False, two=False):
  flow = nx.DiGraph()
  seeds = set()
  for parsed in parse(INPUT):
    code, params = parsed
    if code == 'value':
      val, id = params
      flow.add_node('root'+id+val, val=val, vals=[])
      flow.add_edge('root'+id+val, id)
      seeds.add('root'+id+val)
    elif code == 'bot':
      id, lowtype, low, hightype, high = params
      low_out = 'o'+low if lowtype == 'output' else low
      high_out = 'h'+high if hightype == 'output' else high
      flow.add_node(id, vals=[])
      flow.add_node(high_out, vals=[])
      flow.add_node(low_out, vals=[])
      flow.nodes[id]['high'] = high_out
      flow.nodes[id]['low'] = low_out
      flow.add_edge(id, high_out)
      flow.add_edge(id, low_out)
  for s in seeds:
    out = flow.edges(nbunch=s)
    val = int(flow.nodes[s]['val'])
    for oe in out:
      # print(oe[1])
      flow.nodes[oe[1]]['vals'].append(val)
  prop_count = -1
  propagated = set()
  while prop_count != 0:
    prop_count = 0
    for node_id in flow.nodes:
      node = flow.nodes[node_id]
      if node_id in propagated:
        continue
      if node.get('high', None) != None:
        vals = node['vals']
        if len(vals) == 2:
          low = min(vals); high = max(vals)
          flow.nodes[node['high']]['vals'].append(high)
          flow.nodes[node['low']]['vals'].append(low)
          propagated.add(node_id)
          prop_count += 1
  if not two:
    for (node_id, node) in flow.nodes.items():
      # print(node_id, node['vals'])
      if node['vals'] == [61, 17]:
        return node_id
  else:
    return flow.nodes['o0']['vals'][0] * flow.nodes['o1']['vals'][0] * flow.nodes['o2']['vals'][0]

def two(INPUT): return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "10")

  p.run(one, 0)
  p.run(two, 0)

#!/usr/bin/env python3
import puzzle, math, re

def parse_input(INPUT):
  return INPUT

def puzz(INPUT):

  class Edge(object):
    def __init__(self, a_id, b_id, a_vol, b_vol):
      self.a_id = a_id
      self.b_id = b_id
      self.a_vol = a_vol
      self.b_vol = b_vol
      
  class Node(object):
    def __init__(self, node_id):
      self.in_edges = {}
      self.out_edges = {}
      self.node_id = node_id

    def add_edge(self, edge):
      self.in_edges[edge.a_id] = edge

    def reconcile(self, nodes):
      for edge in self.in_edges.values():
        producer = nodes[edge.a_id]
        producer.out_edges[edge.b_id] = edge

  nodes = {}
  component_pat = "(\\d+) (\\w+)"
  for line in INPUT:
    components = re.findall(component_pat, line)
    inputs = [(int(c[0]), c[1].strip()) for c in components[:-1]]
    b_vol, b_id = int(components[-1][0]), components[-1][1]
    node = nodes.get(b_id, Node(b_id))
    for ip in inputs:
      a_vol, a_id = ip
      edge = Edge(a_id, b_id, a_vol, b_vol)
      node.add_edge(edge)
    nodes[b_id] = node
    nodes["ORE"] = Node("ORE")
  for node in nodes.values():
    node.reconcile(nodes)
  def topological(root, nodes):
    visited_nodes = []
    sorted_nodes = []

    def topological_helper(node):
      if node in sorted_nodes:
        return
      if node in visited_nodes:
        print("ERROR: NOT A DAG")
      visited_nodes.append(node)
      for edge_id in node.in_edges.keys():
        topological_helper(nodes[edge_id])
      visited_nodes.remove(node)
      sorted_nodes.append(node)
    topological_helper(root)
    sorted_nodes.reverse()
    return sorted_nodes

  sorted_nodes = topological(nodes["FUEL"], nodes)

  def needed(fuel):
    needed={}
    needed["FUEL"] = fuel
    for node in sorted_nodes[1:]:
      # print(node.node_id)
      total = 0
      for out in node.out_edges.values():
        # print(out.a_id, out.b_id, out.a_vol, out.b_vol, math.ceil(needed[out.b_id] / out.b_vol) * out.a_vol)
        total += math.ceil(needed[out.b_id] / out.b_vol) * out.a_vol
      needed[node.node_id] = total
    return needed["ORE"]
  
  def needed_too_much(fuel):
    return needed(fuel) > 1000000000000

  fuel = 1
  while not needed_too_much(fuel):
    fuel *= 10
  fuel /= 10
  while not needed_too_much(fuel):
    fuel += 10000
  fuel -= 10000
  while not needed_too_much(fuel):
    fuel += 1000
  fuel -= 1000
  while not needed_too_much(fuel):
    fuel += 100
  fuel -= 100
  while not needed_too_much(fuel):
    fuel += 10
  fuel -= 10
  while not needed_too_much(fuel):
    fuel += 1
  fuel -= 1
  return needed(1) // 1, int(fuel)

def one(INPUT):
  return puzz(INPUT)[0]

def two(INPUT):
  return puzz(INPUT)[1]

if __name__ != '__main':

  p = puzzle.Puzzle("2019", "14")
  p.run(one, 0)
  p.run(two, 0)

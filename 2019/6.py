#!/usr/bin/env python3
import puzzle

class Node(object):
  def __init__(self, name):
    self.name = name
    self.parent = None
    self.children = {}

  def add_child(self, node):
    self.children[node.name] = node

  def total_paths(self, depth):
    tot = depth
    for child_val in self.children.values():
      tot += child_val.total_paths(depth+1)
    return tot

  def parent_chain(self):
    if not self.parent:
      return []
    return [self.parent] + self.parent.parent_chain()

def puzz(INPUT, two=False):
  all_nodes = {}
  for edge in INPUT:
    a_id, b_id = edge.split(')')
    a_id = a_id.strip()
    b_id = b_id.strip()
    a_node = all_nodes.get(a_id, Node(a_id))
    b_node = all_nodes.get(b_id, Node(b_id))
    all_nodes[a_id] = a_node
    all_nodes[b_id] = b_node
    a_node.add_child(b_node)
    b_node.parent = a_node

  me_chain = all_nodes['YOU'].parent_chain()
  san_chain = all_nodes['SAN'].parent_chain()
  if two:
    for i, item in enumerate(me_chain):
      if item in san_chain:
        return i + san_chain.index(item)
  else:
    return all_nodes["COM"].total_paths(0)

def one(INPUT):
  return puzz(INPUT, two=False)

def two(INPUT):
  return puzz(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "6")
  p.run(puzz, 0)
  p.run(two, 0)

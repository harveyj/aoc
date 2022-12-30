#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  G = nx.Graph()
  for l in INPUT.split('\n'):
    op_mat = re.match('(\w+): (\w+) (.) (\w+)', l)
    if op_mat:
      G.add_node(op_mat.group(1), op = op_mat.group(3), l=op_mat.group(2), r=op_mat.group(4))
    else: 
      lit_mat = re.match('(\w+): (\d+)', l)
      G.add_node(lit_mat.group(1), val=int(lit_mat.group(2)))
  return G

def apply(l, r, op):
  if op == '+':
    return l+r
  elif op == '-':
    return l-r
  elif op == '*':
    return l*r
  elif op == '/':
    return l//r

def apply2(l, r, op):
  # a(HUM) + b
  a, b = l
  c, d = r
  if op == '+':
    return (a + c, b + d)
  elif op == '-':
    return (a - c, b - d)
  elif op == '*':
    return (a*d + b*c, b*d)
  elif op == '/':
    if c != 0:
      # b / (cx+d)
      print("ERROR")
    else:
      return(a/d, b/d)


def postorder(G, root, apply):
  l = G.nodes[root].get('l', None)
  r = G.nodes[root].get('r', None)
  if not l:
    return G.nodes[root].get('val')
  else:
    l_val = postorder(G, l)
    r_val = postorder(G, r)
    return apply(l_val, r_val, G.nodes[root].get('op'))

def postorder2(G, root):
  if root == 'humn':
    return (1, 0)
  l = G.nodes[root].get('l', None)
  r = G.nodes[root].get('r', None)
  if not l:
    return (0, G.nodes[root].get('val'))
  else:
    l_val = postorder2(G, l)
    r_val = postorder2(G, r)
    return apply2(l_val, r_val, G.nodes[root].get('op'))


def one(INPUT):
  G = parse(INPUT)
  return postorder(G, 'root')

def two(INPUT):
  G = parse(INPUT)
  l = G.nodes["root"].get('l', None)
  r = G.nodes["root"].get('r', None)
  a, b = postorder2(G, l)
  c, d = postorder2(G, r)
  return (d-b) / a

p = puzzle.Puzzle("21")
# p.run(one, 0)
p.run(two, 0)

import collections
import anytree
import math
import puzzle

def tree(in_list, parent):
  name = in_list if type(in_list) == int else ''
  root = anytree.Node(name=name, parent=parent)
  if type(in_list) == list:
    tree(in_list[0], root)
    tree(in_list[1], root)
  return root

def explode(in_tree):
  leaves = [node for node in anytree.PreOrderIter(in_tree, filter_=lambda n: n.name != '')]
  for i in range(len(leaves)):
    l = leaves[i]
    if l.depth > 4:
      next_l = leaves[i+1]
      if i > 0:
        leaves[i-1].name += l.name
        zero_node = anytree.Node(name=0)
      else:
        l.name = 0
      if i+1 != len(leaves) - 1:
        leaves[i+2].name += next_l.name
      else:
        next_l.name = 0
      parent = l.parent
      zero_node = anytree.Node(name=0)
      l.parent.parent.children = [zero_node if c == parent else c for c in l.parent.parent.children]
      return True
  return False

def split(in_tree):
  leaves = [node for node in anytree.PreOrderIter(in_tree, filter_=lambda n: n.name != '')]
  for leaf in leaves:
    if leaf.name > 9:
      lval = math.floor(leaf.name/2)
      rval = math.ceil(leaf.name/2)
      leaf.name = ''
      anytree.Node(lval, parent=leaf)
      anytree.Node(rval, parent=leaf)
      return True
  return False

def concat(t1, t2):
  root = anytree.Node(name='')
  t1.parent = root
  t2.parent = root
  return root

def add(t1, t2):
  t = concat(t1, t2)
  # print(anytree.RenderTree(t))
  dirty = True
  while dirty:
    dirty = False
    while explode(t):
      dirty = True
      # print("EXPLODE")
      # print(anytree.RenderTree(t))
    if split(t):
      dirty = True
      # print("SPLIT")
      # print(anytree.RenderTree(t))
  return t

def mag(tree):
  if tree.name != '':
    return tree.name
  return mag(tree.children[0])*3 + mag(tree.children[1])*2


def one(INPUT):
  lines = INPUT.split('\n')
  t = tree(eval(lines[0]), None)
  for l in lines[1:]:
    t_n = tree(eval(l), None)
    t = add(t, t_n)
    # print(anytree.RenderTree(t))
  print("PART ONE ANSWER:", mag(t))

def two(INPUT):
  lines = INPUT.split('\n')
  mags = []
  for l1 in lines:
    for l2 in lines:
      mags.append(mag(add(tree(eval(l1), None), (tree(eval(l2), None)))))
  print("PART TWO ANSWER:", max(mags))

p = puzzle.Puzzle("18")
p.run(one, 0)
p.run(two, 0)

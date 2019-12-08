import sys
inlines = open(sys.argv[1]).readlines()

all_nodes = {}

class Node(object):
	def __init__(self, name):
		self.name = name
		self.children = {}

	def add_child(self, node):
		self.children[node.name] = node

	def total_paths(self, depth):
		tot = depth
		for child_val in self.children.values():
			tot += child_val.total_paths(depth+1)
		return tot

for edge in inlines:
	a_id, b_id = edge.split(')')
	a_id = a_id.strip()
	b_id = b_id.strip()
	a_node = all_nodes.get(a_id, Node(a_id))
	b_node = all_nodes.get(b_id, Node(b_id))
	all_nodes[a_id] = a_node
	all_nodes[b_id] = b_node
	a_node.add_child(b_node)

print(all_nodes["COM"].total_paths(0))
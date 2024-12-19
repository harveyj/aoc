import re, sys, math
from collections import defaultdict

class Edge(object):
	def __init__(self, producer_id, consumer_id, producer_vol, consumer_vol):
		self.producer_id = producer_id
		self.consumer_id = consumer_id
		self.producer_vol = producer_vol
		self.consumer_vol = consumer_vol
		
class Node(object):
	def __init__(self, node_id):
		self.forward_edges = {}
		self.back_edges = {}
		self.node_id = node_id

	# def get_needed_consumers(self):
	# 	return [consumer for consumer_key, consumer in self.consumers.items() if not self.nodes[consumer_key].saturated]

# nodes = {}
back_tree = {}
back_tree["ORE"] = []
forward_tree = {}
component_pat = "(\\d+) (\\w+)"
for line in open(sys.argv[1]).readlines():
	components = re.findall(component_pat, line)
	producers = [(int(c[0]), c[1].strip()) for c in components[:-1]]
	consumer_vol, consumer_id = int(components[-1][0]), components[-1][1]
	back_edges = []
	for ip in producers:
		producer_vol, producer_id = ip
		# node = nodes.get(producer_id, Node(producer_id, nodes))
		edge = Edge(producer_id, consumer_id, producer_vol, consumer_vol)
		back_edges.append(edge)
		# nodes[producer_id] = node
	back_tree[consumer_id] = back_edges

	# nodes["FUEL"] = Node("FUEL", nodes)
demands = defaultdict(lambda: 0)
def walk(node_id, mult):
	# walk_edges = []
	for e in back_tree[node_id]:
		print("WALK", e.producer_id, e.consumer_id, e.producer_vol, e.consumer_vol)
		demands[e.producer_id] += math.ceil(e.producer_vol / e.consumer_vol) * mult
		walk(e.producer_id, e.producer_vol * mult)
	# 	walk_edges.append(e)
	# for node in walk_edges:
walk("FUEL", 1)
print(demands)
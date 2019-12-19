import re, sys, math
from collections import defaultdict

class Edge(object):
	def __init__(self, producer_id, consumer_id, producer_vol, consumer_vol):
		self.producer_id = producer_id
		self.consumer_id = consumer_id
		self.producer_vol = producer_vol
		self.consumer_vol = consumer_vol
		
class Node(object):
	def __init__(self, node_id, nodes):
		self.forward_edges = {}
		self.back_edges = {}
		self.node_id = node_id
		self.saturated = node_id == "FUEL"
		self.nodes = nodes
		self.total = 0
		self.used = 0

	def add_edge(self, edge):
		self.forward_edges.append(edge)

	def add_total(self, total):
		if self.saturated: return
		self.total += total
		self.balance()
		# print("ADD_TOTAL", self.node_id)
		if not self.get_needed_consumers():
			self.saturated = True
			print("SATURATED", self.node_id)

	def balance(self):
		def largest_requirement(edge):
			return -1 * edge.consumer_vol
		needed_consumers = self.get_needed_consumers()
		needed_consumers.sort(key=largest_requirement)
		if needed_consumers:
			edge = needed_consumers[0]
			if self.total - self.used_total >= edge.producer_vol:
				self.used_total += edge.consumer_vol
				print("ADD TO", edge.producer_id, edge.consumer_id, edge.producer_vol, edge.consumer_vol)
				self.nodes[edge.consumer_id].add_total(edge.consumer_vol)

	def get_needed_consumers(self, nodes):
		return [consumer for consumer_key, consumer in self.consumers.items() if not self.nodes[consumer_key].saturated]

nodes = {}
component_pat = "(\\d+) (\\w+)"
for line in open(sys.argv[1]).readlines():
	components = re.findall(component_pat, line)
	producers = [(int(c[0]), c[1].strip()) for c in components[:-1]]
	consumer_vol, consumer_id = int(components[-1][0]), components[-1][1]
	for ip in producers:
		producer_vol, producer_id = ip
		node = nodes.get(producer_id, Node(producer_id))
		edge = Edge(producer_id, consumer_id, producer_vol, consumer_vol)
		node.add_edge(edge)
		nodes[producer_id] = node
	nodes["FUEL"] = Node("FUEL", nodes)


import sys
import copy
import collections

class Grid(object):

	def __init__(self, width=50, height=50, grid=None):
		self.floor = copy.deepcopy(grid)
		self.width = len(grid[0])
		self.height = len(grid)
		self.loc = None
		self.keys = {}
		self.keys_rev = {}
		self.doors = {}

	def scrub_18(self):
		for x in range(self.width):
			for y in range(self.height):
				cell = self.get((x, y), [])
				if cell == "@":
					self.loc = (x, y)
					self.set((x,y), ".")
				elif cell in list("abcdefghijklmnopqrstuvwxyz@"):
					# Convention: '.' is the only navigable terrain
					self.keys[cell] = (x, y)
					self.keys_rev[(x, y)] = cell
					self.set((x,y), ".")
				elif cell in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
					self.doors[cell] = (x, y)

	def get(self, loc, accessed_keys):
		if loc[1] >= len(self.floor) or loc[0] >= len(self.floor[0]) or loc[0] < 0 or loc[1] < 0:
			return '#'
		if self.floor[loc[1]][loc[0]].lower() in accessed_keys:
			return '.'
		return self.floor[loc[1]][loc[0]]

	def set(self, loc, val):
		self.floor[loc[1]][loc[0]] = val

	def __str__(self):
		floor = copy.deepcopy(self.floor)
		overlay_pts = [(loc, val) for (val, loc) in self.keys.items()]
		overlay_pts += [(self.loc, '@')]

		print(overlay_pts)
		for p in overlay_pts:
			floor[p[0][1]][p[0][0]] = p[1]
		rets = []
		for l in floor:
			rets.append(''.join(l))
		return '\n'.join(rets)

	def preprocess_graph(self):
		nodes = {}
		for x in range(self.width):
			for y in range(self.height):
				if self.get((x, y), []) != '#':
					for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
						nx, ny = x + dx, y + dy
						print('.', end='')
						if self.get((nx, ny), []) != '#':
							outs = nodes.get((x, y), [])
							outs.append((nx, ny))
							nodes[(x, y)] = outs
		print(nodes[self.loc])
		final_nodes = {}
		q = collections.deque(nodes[self.loc])
		seen = set()
		while q:
			node = q.popleft()
			start = node
			def find_end(node):
				print(node)
				seen = set()
				while True:
					outs = [n for n in nodes[node] if not node in seen]
					seen.add(node)
					if len(outs) == 0:
						return None
					elif len(outs) == 1:
						node = list(seen)[0]
					else:
						return node
			for out in nodes[node]:
				if out in seen:
					continue
				seen.add(out)
				end = find_end(out)
				if not end:
					continue
				for n in nodes[end]: q.append(n)
				outs = final_nodes.get(start, [])
				outs.append(end)
				final_nodes[start] = outs
		return nodes

def distance_to_keys(current_key, keys, found_keys, cache):
	def distance(target, parents):
		node = target
		path = []
		while node in parents:
			path.append(node)
			node = parents[node]
		return len(path) - 1

	if len(found_keys) == len(keys):
		print("end!")
		return 0

	cache_key = current_key + str(frozenset(found_keys))
	if cache_key in cache:
		# print('returning', cache_key, cache[cache_key])
		return cache[cache_key]
	reachable_keys, parents = grid.bfs(grid.keys[current_key], found_keys + [current_key])
	cost = 10000000000000000
	real_reachables = [rk for rk in reachable_keys if not rk in found_keys + [current_key]]
	# print('dtk', current_key, keys, found_keys, real_reachables)
	cheapest_next = None
	for next_key in real_reachables:
		new_cost = (distance(grid.keys[next_key], parents) +
				    distance_to_keys(next_key, keys, found_keys+[current_key], cache))
		if new_cost < cost:
			cost = new_cost
			cheapest_next = next_key
		# print(distance(next_key, parents))
		# print(cost, found_keys+[current_key])
	print("cheapest", current_key, cheapest_next, cost)
	cache[cache_key] = cost
	return cost

grid_raw = []
for line in open(sys.argv[1]):
	grid_raw.append(list(line.strip()))

grid = Grid(grid=grid_raw)
grid.scrub_18()
keys = list(grid.keys.keys())
cache = {}
# cost = distance_to_keys('@', keys, [], cache)
print(grid.preprocess_graph())
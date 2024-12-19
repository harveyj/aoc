import sys
import copy
import collections

class Grid(object):

	def __init__(self, width=50, height=50, grid=None):
		if grid:
			self.width = len(grid[0])
			self.height = len(grid)
			self.floor = copy.deepcopy(grid)
		else:
			self.floor = [[' ' for i in range(height)] for j in range(width)]
		
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
				elif cell in list("abcdefghijklmnopqrstuvwxyz"):
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


	def graph(self, start_loc):
		class Node(object):
			def __init__(self, loc, data):
				# id (string) --> Node, cost
				self.out = {}
				self.loc = loc
				self.data = data

		nodes = {} # id, node
		queue = [start_loc]
		seen = []
		i = 0
		nodes[i] = Node()
		while i < len(queue):
			loc = queue[i]
			i += 1
			if loc in seen:
				continue


	def bfs(self, start_loc, accessed_keys):
		def north(loc): return loc[0], loc[1] - 1
		def south(loc): return loc[0], loc[1] + 1
		def east(loc): return loc[0] + 1, loc[1]
		def west(loc): return loc[0] - 1, loc[1]


		queue = [start_loc]
		seen = []
		seen_keys = []
		parents = {start_loc: None}
		i = 0
		while i < len(queue):
			loc = queue[i]
			i += 1
			if loc in seen:
				continue
			if loc in self.keys_rev and self.keys_rev[loc] not in accessed_keys:
				seen_keys.append(self.keys_rev[loc])
				continue
			seen.append(loc)
			for new_loc in [north(loc), south(loc), east(loc), west(loc)]:
				if self.get(new_loc, accessed_keys) == '.' and not new_loc in seen:
						parents[new_loc] = loc
						queue.append(new_loc)

		return seen_keys, parents


class Bot(object):
	def __init__(self, loc):
		self.loc = loc
		# These are uppercase to correspond with the door
		self.accessed_keys = []

	def path(self, target, parents):
		node = target
		path = []
		while node != self.loc:
			path.append(node)
			node = parents[node]
		return path

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
bot = Bot(grid.loc)
keys = list(grid.keys.keys())
grid.keys['@'] = grid.loc
grid.keys_rev[grid.loc] = '@'
cache = {}
print(grid.keys.keys())
cost = distance_to_keys('@', keys, [], cache)
print(cost)
print(cache)

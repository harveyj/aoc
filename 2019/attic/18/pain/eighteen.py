import sys
import copy

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
		if self.floor[loc[1]][loc[0]] in accessed_keys:
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

	def bfs(self, start_loc, accessed_keys):
		def north(loc): return loc[0], loc[1] - 1
		def south(loc): return loc[0], loc[1] + 1
		def east(loc): return loc[0] + 1, loc[1]
		def west(loc): return loc[0] - 1, loc[1]

		accessed_keys = [k.upper() for k in accessed_keys]

		queue = [start_loc]
		seen = set()
		seen_keys = {}
		parents = {start_loc: None}
		i = 0
		while i < len(queue):
			loc = queue[i]
			i += 1
			if loc in seen:
				continue
			if loc in self.keys_rev:
				seen_keys[self.keys_rev[loc]] = loc
			seen.add(loc)
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

def naive(grid, bot):
	keys_to_find = len(grid.keys)
	bot.accessed_keys = []
	total_len = 0
	while len(bot.accessed_keys) < keys_to_find:
		seen_keys, parents = grid.bfs(bot.loc, bot.accessed_keys)
		best_key = None
		best_len = 1000000000000
		for sk in seen_keys:
			if sk.upper() in bot.accessed_keys: continue
			path_len = len(bot.path(grid.keys[sk], parents))
			if path_len < best_len:
				print("keeping", path_len)
				best_key = sk
				best_len = path_len
		total_len += best_len

		bot.accessed_keys += [best_key.upper()]
		bot.loc = grid.keys[best_key]

def all_paths(grid, bot):
	keys_to_find = len(grid.keys)
	paths = [[]]
	while len(paths[0]) < keys_to_find:
		new_paths = []
		for p in paths:
			seen_keys, parents = grid.bfs(bot.loc, p)
			for sk in seen_keys:
				if sk in p:
					continue
				new_paths.append(p + [sk])
		paths = new_paths
		print(len(paths))
	return paths


grid_raw = []
for line in open(sys.argv[1]):
	grid_raw.append(list(line.strip()))

grid = Grid(grid=grid_raw)
grid.scrub_18()
bot = Bot(grid.loc)

ap = all_paths(grid, bot)
print(len(ap))
# naive(grid, bot)
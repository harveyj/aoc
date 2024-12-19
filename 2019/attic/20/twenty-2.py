import fileinput, itertools, collections, copy
import heapq

class Grid(object):

	def __init__(self):
		self.floor = [list(line[:-1]) for line in fileinput.input()]
		self.width = len(self.floor[0])
		self.height = len(self.floor)
		self.portals = {}
		self.portal_locs = {}
		self.portal_keys = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!']
		self.next_portal_key = 0
		self.overlay_pts = []
		self.scrub()

	def scrub(self):
		for x in range(self.width):
			for y in range(self.height):
				c = self.get(x, y)
				# This is a monster and i hate it
				if c.isupper():
					key = ''
					c1, c2, c3 = self.get(x, y), self.get(x, y + 1), self.get(x, y+2)
					if c2 != '#' and c3 == '.':
						key = c1+c2
						key_loc = x, y + 2 
						self.set(x, y, '#')
						self.set(x, y + 1, '#')
					c1, c2, c3 = self.get(x, y), self.get(x+1, y), self.get(x+2, y)
					if c2 != '#' and c3 == '.':
						key = c1+c2
						key_loc = x + 2, y 
						self.set(x, y, '#')
						self.set(x+1, y, '#')
					c1, c2, c3 = self.get(x-1, y), self.get(x, y), self.get(x+1, y)
					if c2 != '#' and c1 == '.':
						key = c2+c3
						key_loc = x-1, y 
						self.set(x, y, '#')
						self.set(x + 1, y, '#')
					c1, c2, c3 = self.get(x, y-1), self.get(x, y), self.get(x, y+1)
					if c2 != '#' and c1 == '.':
						key_loc = x, y-1
						key = c2+c3
						self.set(x, y, '#')
						self.set(x, y + 1, '#')
					if key not in self.portals:
						self.portals[key] = self.portal_keys[self.next_portal_key]
						self.next_portal_key += 1
					key = self.portals[key]
					kx, ky = key_loc
					self.portal_locs[(kx, ky)] = key
					self.set(kx, ky, key)

	def get(self, x, y):
		if y >= len(self.floor) or x >= len(self.floor[0]) or y < 0 or x < 0:
			return '#'
		return self.floor[y][x]

	def set(self, x, y, val):
		self.floor[y][x] = val

	def __str__(self):
		floor = copy.deepcopy(self.floor)
		if self.overlay_pts:
			print(self.overlay_pts[0])
			floor[self.overlay_pts[0][0][0]][self.overlay_pts[0][0][1]] = self.overlay_pts[0][1]
		rets = []
		for l in floor:
			rets.append(''.join(l))
		rets = '\n'.join(rets)
		rets = rets.replace("#", " ")
		return rets

def outer(grid, x, y):
	if x < 6 or y < 6 or x > grid.width -6 or y > grid.height - 6:
		return True
	return False

def bfs(grid, x, y, ex, ey):
	queue = collections.deque([(x, y, 0)])
	seen = set((x, y, 0))
	parents = {}
	while queue:
		x, y, level = queue.popleft()
		seen.add((x, y, level))
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx, ny = x + dx, y + dy
			if ((nx, ny, level)) in seen:
				continue
			seen.add((nx, ny, level))

			c = grid.get(nx, ny)

			if c == '.':
				queue.append((nx, ny, level))
				parents[(nx, ny, level)] = x, y, level
			elif c != '#':
				parents[(nx, ny, level)] = x, y, level
				px, py = get_portal_loc(grid, (nx, ny))
				if (px, py) == (-1, -1):
					if (nx, ny) == (ex, ey) and level == 0:
						parents[(nx, ny, level)] = x, y, level
						print("END")
						return parents
				else:
					if outer(grid, nx, ny) and level > 0:
						queue.append((px, py, level - 1))
						parents[(px, py, level - 1)] = nx, ny, level
						print("TELEPORT", nx, ny, level, px, py, level-1)
					elif not outer(grid, nx, ny):
						queue.append((px, py, level + 1))
						parents[(px, py, level + 1)] = nx, ny, level
						print("TELEPORT", nx, ny, level, px, py, level+1)


	return parents

def get_portal_loc(grid, my_loc):
	my_code = None
	for loc, code in grid.portal_locs.items():
		if loc == my_loc:
			my_code = code
	for loc, code in grid.portal_locs.items():
		if code == my_code and loc != my_loc:
			return loc
	return (-1, -1)


grid = Grid()
print(grid.portal_locs)
sx, sy = -1, -1
for (x, y) in grid.portal_locs.keys():
	if grid.portal_locs[x, y] == grid.portals['AA']:
		sx, sy = x, y
	if grid.portal_locs[x, y] == grid.portals['ZZ']:
		ex, ey = x, y
parents = bfs(grid, sx, sy, ex, ey)
parents[sx, sy, 0] = None

node = parents[ex, ey, 0]
pathlen = 0
# print(parents)
while node:
	# if grid.get(node[0], node[1]) == '.':
	# 	grid.set(node[0], node[1], '*')
	print(node)
	node = parents[node]
	pathlen += 1
print(grid)
print(pathlen)

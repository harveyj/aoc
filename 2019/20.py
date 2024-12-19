#!/usr/bin/env python3
import puzzle
import collections, copy

class Grid(object):

	def __init__(self, INPUT):
		self.floor = [list(line[:-1]) for line in INPUT]
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


def bfs(grid, x, y, ex, ey):
	queue = collections.deque([(x, y)])
	seen = set((x, y))
	parents = {}
	while queue:
		x, y = queue.popleft()
		seen.add((x, y))
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx, ny = x + dx, y + dy
			if (nx, ny) == (ex, ey):
				parents[(nx, ny)] = x, y
				print("END")
			if ((nx, ny)) in seen:
				continue
			seen.add((nx, ny))
			parents[(nx, ny)] = x, y

			c = grid.get(nx, ny)

			if c == '.':
				queue.append((nx, ny))
			elif c != '#':
				px, py = get_portal_loc(grid, (nx, ny))
				if (px, py) != (-1, -1):
					parents[(px, py)] = nx, ny
					queue.append((px, py))

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

# Test get_portal_loc
# for loc, code in g.portal_locs.items():
# 	print(loc, code, get_portal_loc(g, loc))


def one(INPUT):
  grid = Grid(INPUT)
  sx, sy = -1, -1
  for (x, y) in grid.portal_locs.keys():
    if grid.portal_locs[x, y] == grid.portals['AA']:
      sx, sy = x, y
    if grid.portal_locs[x, y] == grid.portals['ZZ']:
      ex, ey = x, y
  parents = bfs(grid, sx, sy, ex, ey)
  parents[sx, sy] = None

  node = parents[ex, ey]
  pathlen = 0
  while node:
    if grid.get(node[0], node[1]) == '.':
      grid.set(node[0], node[1], '*')
    node = parents[node]
    pathlen += 1
  print(grid)
  print(pathlen)

  invals = parse_input(INPUT)
  out = 0
  return out

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "20")

  p.run(one, 0)
  p.run(two, 0)

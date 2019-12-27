import fileinput, itertools, collections, copy
import heapq

def reachable_keys(grid, x, y, dest):
	queue = collections.deque()
	queue.append((x, y, 0))
	seen = set()
	while queue:
		x, y, cost = queue.popleft()
		if grid[y][x].islower() and grid[y][x] not in keys:
			yield cost, x, y, grid[y][x]
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx, ny = x + dx, y + dy
			if ((nx, ny)) in seen:
				continue
			seen.add((nx, ny))
			c = grid[ny][nx]

			if c != '#' and (not c.isupper() or c.lower() in keys):
				queue.append((nx, ny, cost + 1))

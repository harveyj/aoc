# heavily indebted - https://www.reddit.com/r/adventofcode/comments/ec8090/2019_day_18_solutions/

import fileinput, itertools, collections, copy
import heapq

grid = [list(line.strip()) for line in fileinput.input()]
lingrid = list(itertools.chain.from_iterable(grid))
ALL_KEYS = set([c for c in lingrid if c.islower()])
linstart = lingrid.index('@')
w, h = len(grid[0]), len(grid)
sx, sy = linstart % w, linstart // w

# Transform for part 2
grid[sy-1][sx] = '#'
grid[sy+1][sx] = '#'
grid[sy][sx-1] = '#'
grid[sy][sx]   = '#'
grid[sy][sx+1] = '#'

pos = (((sx-1), (sy-1)), ((sx+1), (sy-1)), ((sx-1), (sy+1)), ((sx+1), (sy+1)))

render_grid = copy.copy(grid)
for loc in pos:
	print(loc)
	px, py = loc
	render_grid[py][px] = '@'
for l in render_grid:
	print(''.join(l))

def reachable_keys(grid, x, y, accessed_keys):
	queue = collections.deque()
	queue.append((x, y, 0))
	seen = set()
	# parents = {(x, y): None}
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
				# parents[(nx, ny)] = (x, y)
				queue.append((nx, ny, cost + 1))

queue = [(0, pos, frozenset())]
seen = set()
while queue:
	cost, cpos, keys = heapq.heappop(queue)
	print(cost, cpos, keys)
	if len(keys) == len(ALL_KEYS):
		print("TERM END")
		print(cost)
		break
	if (cpos, keys) in seen:
		continue
	seen.add((cpos, keys))
	for i, (cx, cy) in enumerate(cpos):
		for sub_cost, nx, ny, key in reachable_keys(grid, cx, cy, keys):
			npos = cpos[0:i] + ((nx, ny),) + cpos[i+1:]
			heapq.heappush(queue, (cost + sub_cost, npos, keys | frozenset([key])))
print("END QUEUE")

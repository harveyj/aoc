import fileinput, itertools, collections
grid = [list(line.strip()) for line in fileinput.input()]
lingrid = list(itertools.chain.from_iterable(grid))
ALL_KEYS = set([c for c in lingrid if c.islower()])
linstart = lingrid.index('@')
w, h = len(grid[0]), len(grid)

sx, sy = linstart % w, linstart // w
grid[sy][sx] = '.'
keylocs = {'@': (sx, sy)}
for c in ALL_KEYS:
	start = lingrid.index(c)
	keylocs[c] = start % w, start // w


def bfs(grid, start_loc, accessed_keys):
	def north((x, y)): return x, y - 1
	def south((x, y)): return x, y + 1
	def east((x, y)): return x+1, y
	def west((x, y)): return x-1, y

	queue = collections.deque()
	queue.append(start_loc)
	seen = set()
	parents = {start_loc: None}
	seen_keys = {}
	while queue:
		loc = queue.popleft()
		if loc in seen:
			continue
		seen.add(loc)
		for nx, ny in [north(loc), south(loc), east(loc), west(loc)]:
			c = grid[ny][nx]
			if (c == '.'  or c.lower() in accessed_keys or c.islower()) and not (nx, ny) in seen:
				parents[(nx, ny)] = loc
				if c.islower() and not c in accessed_keys:
					yield parents, c, loc
				queue.append((nx, ny))

def distance(target, parents):
	length = 0
	while target in parents:
		target = parents[target]
		length += 1
	return length

def distance_to_collect_keys(current_key, keys, cache):
	unfound_keys = set(ALL_KEYS)
	unfound_keys.difference_update(keys)
	if not keys: return 0
	cache_key = (current_key, frozenset(keys))
	if cache_key in cache:
		# print('returning ', cache_key)
		print '.',
		return cache[cache_key]

	min_cost = 100000000000000
	for parents, seen_key_val, seen_key_loc in bfs(grid, keylocs[current_key], unfound_keys):
		remaining_keys = set(keys)
		remaining_keys.remove(seen_key_val)
		next_cost = (distance(seen_key_loc, parents) +
		             distance_to_collect_keys(seen_key_val, remaining_keys, cache))
		# print(current_key, seen_key_val, distance(seen_key_loc, parents))
		min_cost = min(min_cost, next_cost)
	cache[cache_key] = min_cost
	return min_cost

cache = {}
# print(bfs(grid, (sx, sy), []))
print(distance_to_collect_keys('@', ALL_KEYS, cache))

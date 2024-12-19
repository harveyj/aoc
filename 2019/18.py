#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  import itertools, collections
  grid = [list(line.strip()) for line in INPUT]
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
    def north(loc): return loc[0], loc[1] - 1
    def south(loc): return loc[0], loc[1] + 1
    def east(loc): return loc[0]+1, loc[1]
    def west(loc): return loc[0]-1, loc[1]

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
      # print '.',
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
  return distance_to_collect_keys('@', ALL_KEYS, cache)


def two(INPUT):
  import fileinput, itertools, collections, copy
  import heapq

  grid = [list(line.strip()) for line in INPUT]
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
    # print(loc)
    px, py = loc
    render_grid[py][px] = '@'
  # for l in render_grid:
  #   print(''.join(l))

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
    # print(cost, cpos, keys)
    if len(keys) == len(ALL_KEYS):
      # print("TERM END")
      return cost
    if (cpos, keys) in seen:
      continue
    seen.add((cpos, keys))
    for i, (cx, cy) in enumerate(cpos):
      for sub_cost, nx, ny, key in reachable_keys(grid, cx, cy, keys):
        npos = cpos[0:i] + ((nx, ny),) + cpos[i+1:]
        heapq.heappush(queue, (cost + sub_cost, npos, keys | frozenset([key])))
  return cost
  print("END QUEUE")

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "18")
  p.run(one, 0)
  p.run(two, 0)

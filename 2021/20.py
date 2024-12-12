from collections import *

def k(x, y):
	return '%i,%i' %(x, y)

def puzz(INPUT):
	table_raw, grid_raw = '\n'.join(INPUT).split("\n\n")
	table = list(table_raw)
	grid = {}
	grid_lines = grid_raw.split("\n")
	min_x, min_y = 0, 0
	max_x, max_y = len(grid_lines[0])+1, len(grid_lines) + 1
	for y, row in enumerate(grid_lines):
		for x, c in enumerate(row):
			if c == '#':
				grid[k(y, x)] = c

	def adjacents(x, y):
		for dx in [-1, 0, 1]:
			for dy in [-1, 0, 1]:
				yield k(x+dx, y+dy)

	for i in range(50):
		new_grid = {}
		for x in range(min_x - 130, max_x+130):
			for y in range(min_y - 130, max_y+130):
				neighbors = [grid.get(key, '') for key in adjacents(x, y)]
				bits = ['1' if n == '#' else '0' for n in neighbors]
				new_idx = int(''.join(bits), 2)
				new_bit = table[new_idx]
				if new_bit == '#':
					new_grid[k(x,y)] = '#'
		grid = new_grid

	total = 0
	for x in range(min_x - 65, max_x+65):
		for y in range(min_x-65, max_y+65):
			print(grid.get(k(x, y), '.'), end='')
			if grid.get(k(x,y)) == '#':
				total += 1
		print("\n", end='')
	print("PART TWO ANSWER", total)
	return total

def one(INPUT):
	return puzz(INPUT)

def two(INPUT):
	return puzz(INPUT)
import sys, math
from itertools import chain

lines = open(sys.argv[1]).readlines()
pts = []
grid = [['.' for i in range(len(lines[0]))] for j in range(len(lines))]

for i, l in enumerate(lines):
	for j, k in enumerate(l):
		if k == '#':
			pts.append((j, i))
			grid[i][j] = '#'

def find_closest(pt1, ptarray):
	closest = ptarray[0]
	for p in ptarray:
		min_dist = abs(closest[0] - pt1[0]) + abs(closest[1] - pt1[1])
		cur_dist = abs(p[0] - pt1[0]) + abs(p[1] - pt1[1])
		if min_dist < cur_dist:
			closest = p

	return p

pt1 = (20, 19)
# pt1 = (11, 13)
# # pt1 = (8, 3)

grid[pt1[1]][pt1[0]] = "X"
angles_to_points = {}
for pt2 in pts:
	if pt1 == pt2: continue
	angle = math.atan2((pt1[0]-pt2[0]), (pt1[1] - pt2[1]))
	points = angles_to_points.get(angle, [])
	points.append(pt2)
	angles_to_points[angle] = points

angles = list(angles_to_points.keys())
angles.sort()
angles.reverse()
i = 0
while angles[i] > 0:
	i += 1
angles = angles[i:] + angles[:i]

num_destroyed = 0
for i, angle in chain(enumerate(angles), enumerate(angles)):
	num_destroyed += 1
	closest = find_closest(pt1, angles_to_points[angle])
	angles_to_points[angle].remove(closest)
	grid[closest[1]][closest[0]] = str(i)
	print("destroyed", num_destroyed, closest)


for l in grid:
	print(''.join(l))

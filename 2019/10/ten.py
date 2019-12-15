import sys, math
lines = open(sys.argv[1]).readlines()
pts = []

for i, l in enumerate(lines):
	for j, k in enumerate(l):
		if k == '#':
			pts.append((j, i))

max_angles = 0
for pt1 in pts:
	angles = []
	for pt2 in pts:
		if pt1 == pt2: continue
		angle = math.atan2((pt1[1]-pt2[1]), (pt1[0] - pt2[0]))

		if angle not in angles:
			angles.append(angle)
	if len(angles) > max_angles:
		max_angles = len(angles)
		print(max_angles, pt1)
# print(pts)
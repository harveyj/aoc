import input22, re
INPUT=input22.INPUT_FULL

marked = {}
for l in INPUT:
	match = re.search("(.*) .=(.*)\.\.(.*),.=(.*)\.\.(.*),.=(.*)\.\.(.*)", l) #"
	sig = 1 if match.group(1) == 'on' else 0
	x1, x2, y1, y2, z1, z2 = map(int, match.group(2, 3, 4, 5, 6, 7))
	if x1 > 50 or x1 < -50: continue
	for x in range(x1, x2+1):
		for y in range(y1, y2+1):
			for z in range(z1, z2+1):
				marked[(x, y, z)] = sig
	print(x1, x2, y1, y2)
print(len(list(filter(lambda a: a, marked.values()))))
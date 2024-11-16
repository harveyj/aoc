import sys
intext = open(sys.argv[1]).read()

WIDTH = 25
HEIGHT = 6

layers = {}
img = [[2 for i in range(WIDTH)] for j in range(HEIGHT)]

for i, c in enumerate(intext):
	c = int(c)
	layer_id = i // (WIDTH * HEIGHT)
	cell_id = i % (WIDTH * HEIGHT)
	layer = layers.get(layer_id, [[0 for i in range(WIDTH)] for j in range(HEIGHT)])

	if img[cell_id // WIDTH][cell_id % WIDTH] == 2:
		img[cell_id // WIDTH][cell_id % WIDTH] = c

	layers[layer_id] = layer

for l in img:
	for c in l:
		if c == 1:
			print('X', end='')
		else:
			print(' ', end='')
	print('')

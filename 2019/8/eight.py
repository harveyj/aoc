import sys
intext = open(sys.argv[1]).read()

WIDTH = 25
HEIGHT = 6

layers = {}

for i, c in enumerate(intext):
	c = int(c)
	layer = i // (WIDTH * HEIGHT)
	layer_hist = layers.get(layer, {})
	char_count = layer_hist.get(c, 0)
	layer_hist[c] = char_count + 1
	layers[layer] = layer_hist

min_zeroes = 100000000000000000
ones_twos = 0
for k in layers:
	zeroes = layers[k][0]
	if zeroes < min_zeroes:
		print(k)
		min_zeroes = zeroes
		ones_twos = layers[k][1]*layers[k][2]
print(ones_twos)
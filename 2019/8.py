#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  WIDTH = 25
  HEIGHT = 6

  layers = {}

  for i, c in enumerate(INPUT[0]):
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
      min_zeroes = zeroes
      ones_twos = layers[k][1]*layers[k][2]
  return ones_twos

def two(INPUT):
  WIDTH = 25
  HEIGHT = 6

  layers = {}
  img = [[2 for i in range(WIDTH)] for j in range(HEIGHT)]

  for i, c in enumerate(INPUT[0]):
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
  return 'FGJUZ'

p = puzzle.Puzzle("2019", "8")
p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle, library
import operator, itertools, networkx as nx

def rotate(l, n):
  return l[n:] + l[:n]

# Copied from 10
def knothash_round(vals, lengths, skip_size=0, offset=0):
  for l in lengths:
    if l != 0:
      vals = rotate(vals, (offset) % len(vals))
      vals = vals[l-1::-1] + vals[l:]
      vals = rotate(vals, -((offset)% len(vals)))
    offset += l + skip_size
    skip_size += 1
  return vals[0]*vals[1], vals, offset, skip_size

def hexchr(i):
  return '0123456789abcdef'[i]

def print_hex(vals):
  ret = ''
  for val in vals:
    ret += hexchr(val // 16) + hexchr(val % 16)
  return ret

def knothash(INPUT):
  key = list(map(ord, INPUT)) + [17, 31, 73, 47, 23]
  vals = list(range(256))
  offset = 0; skip_size = 0
  for i in range(64):
    _, vals, offset, skip_size = knothash_round(vals, key, skip_size, offset)
  dense = []
  for i in range(len(vals) // 16):
    dense.append(list(itertools.accumulate(vals[i*16:(i+1)*16], operator.xor))[-1])
  return print_hex(dense)

def bitstring(hex_string):
  integer_value = int(hex_string, 16)
  bitstring = bin(integer_value)[2:] # strip off leading two chars
  bitstring = bitstring.zfill(len(hex_string) * 4)
  return bitstring

def one(INPUT):
  key = INPUT[0]
  total = 0
  for y in range(128):
    row_key = f'{key}-{y}'
    row = bitstring(knothash(row_key))
    total += str(row).count('1')
  return total

def two(INPUT):
  key = INPUT[0]
  G = library.Grid(x=128, y=128)
  graph = nx.Graph()
  for y in range(G.max_y()):
    row_key = f'{key}-{y}'
    row = str(bitstring(knothash(row_key)))
    for x, c in enumerate(row):
      if c == '1':
        G.set((x, y), 1)
        graph.add_node((x, y))
        if G.get((x, y-1)) == 1:
          graph.add_edge((x, y), (x, y-1))
        if G.get((x-1, y)) == 1:
          graph.add_edge((x, y), (x-1, y))
  return len(list(nx.connected_components(graph)))

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "14")

  p.run(one, 0)
  p.run(two, 0)

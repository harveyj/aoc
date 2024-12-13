from collections import defaultdict
import functools
import operator

# Part 1

def hextobin(h):
  return bin(int(h, 16))[2:].zfill(len(h) * 4)

def decode_packet(bits):
  version, type_id  = int(bits[0:3],2), int(bits[3:6],2)
  if type_id == 4:
    i = 6
    num = []
    while(bits[i] == '1'):
      num.append(bits[i+1:i+5])
      i += 5
    num.append(bits[i+1:i+5])
    val = int(''.join(num), 2)
    return ((version, 'LITERAL', val), i+5)
  else:
    ltid = int(bits[6],2)
    num_subp = 10000000
    num_subp_bits = 10000000
    base_bits_consumed = 7
    sub_bits_consumed = 0
    sub = []
    if ltid:
      num_subp = int(bits[7:18], 2)
      base_bits_consumed += 11
    else:
      num_subp_bits = int(bits[7:22],2)
      base_bits_consumed += 15 
    while len(sub) < num_subp and sub_bits_consumed < num_subp_bits:
      inst, consumed = decode_packet(bits[base_bits_consumed + sub_bits_consumed:])
      sub.append(inst)
      sub_bits_consumed += consumed
    
    return (version, type_id, sub), base_bits_consumed+sub_bits_consumed

def sum_ids(tree):
  tot = tree[0]
  if type(tree[2]) is not list:
    return tot
  for node in tree[2]:
    tot += sum_ids(node)
  return tot

### Part 2

def apply(tree): 
  def op(opcode):
    if opcode == 0:
      return operator.add
    elif opcode == 1:
      return operator.mul
    elif opcode == 2:
      return lambda a, b: b if a > b else a
    elif opcode == 3:
      return lambda a, b: a if a > b else b
    elif opcode == 5:
      return lambda a, b: 1 if a > b else 0
    elif opcode == 6:
      return lambda a, b: 0 if a >= b else 1
    elif opcode == 7:
      return lambda a, b: 1 if a == b else 0
  if type(tree[2]) is not list:
    return tree[2]
  nodes = map(apply, tree[2])
  tot = functools.reduce(op(tree[1]), nodes)
  return tot

def one(INPUT):
  p, bits = decode_packet(hextobin(INPUT[0]))
  # p=(6, 6, [(5, 'LITERAL', 15), (2, 'LITERAL', 15)])
  tot = apply(p)
  # print(p)
  # print(tot)
  return tot

def two(INPUT):
  return one(INPUT)
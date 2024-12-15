#!/usr/bin/env python3
import puzzle

# FULL ALU IMPLEMENTATION - only used to check things in the end.
# https://appdividend.com/2021/03/23/how-to-check-if-string-is-integer-in-python/
def checkInt(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()

class ALU(object):
  def __init__(self, inputs=[]):
    self.inputs = inputs
    self.regs = {'w':0, 'x':0, 'y':0, 'z':0}

  def run(self, prog):
    for line in prog.split("\n"):
      self.exec(line)
      # print(self.regs)

  def exec(self, inst):
    op, a = inst.split(" ")[:2]
    if op == "inp":
      self.regs[a] = self.inputs.pop(0)
      return
    b = inst.split(" ")[2]
    if checkInt(b):
      b = int(b)
    else: b = self.regs[b]
    if op == "add":
      self.regs[a] += b
    elif op == "mul":
      self.regs[a] *= b
    elif op == "div":
      self.regs[a] //= b
    elif op == "mod":
      self.regs[a] %= b
    elif op == "eql":
      self.regs[a] = 1 if self.regs[a] == b else 0

# Decompilation
# Line by line translation
def iter_z(in_val, z, add_x, add_y, div_z):
  w = in_val
  x = z % 26
  z //= div_z
  x += add_x
  x = 0 if x == w else 1
  y = 25
  y *= x
  y += 1
  z *= y
  y = w + add_y
  y *= x
  z += y
  return z

# One-liner
def iter_z_2(w, z, add_x, add_y, div_z):
  # print('if', 0 if z % 26 + add_x == w else 1)
  return z // div_z * (25 * (0 if z % 26 + add_x == w else 1) + 1) + (w + add_y) * (0 if z % 26 + add_x == w else 1)

# Back out the one-liner for readability
def iter_z_3(w, z, add_x, add_y, div_z):
  if (z % 26 + add_x) == w:
    return z // div_z 
  else:
    return z // div_z * 26 + (w+add_y)

# Full copy of the ASM program. 
# slice: just run the first $SLICE cycles,
def python_version(inputs, z_start=0, slice=14):
  x_s = [12, 11, 13, 11, 14, -10, 11, -9, -3, 13, -5, -10, -4, -5][:slice]
  y_s = [4, 11, 5, 11, 14, 7, 11, 4, 6, 5, 9, 12, 14, 14][:slice]
  z_s = [1, 1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 26, 26, 26][:slice]
  z = z_start
  for w_in, x_in, y_in, z_in in zip(inputs, x_s, y_s, z_s):
    z = iter_z_3(w_in, z, x_in, y_in, z_in)
  return z

# Utility functions
def simple_run(INPUT, user_input):
  alu = ALU(user_input)
  alu.run(INPUT)
  return alu

def simple_run_last_segment(INPUT):
  for digit in range(1, 10):
    for z in range(0, 200):
      alu = ALU([digit])
      alu.regs['z'] = z
      alu.run(INPUT)
      if alu.regs['z'] == 0:
        print(digit, z, alu.regs['z'])

def assert_eq(user_input):
  alu = puzzle.Puzzle("24").run(simple_run, 0, user_input)
  if alu.regs["z"] != python_version(user_input):
    print("FAIL", alu.regs["z"],python_version(user_input))
  if alu.regs["z"] == 0:
    print("ZERO", user_input)

def base_26(val):
  return [val // (26 ** n) % 26 for n in range(7, -1, -1)]

# MAIN CODE: Discover and print out the constraints. 

two = lambda a: one(a)
def one(INPUT):
  x_s = [0, 12, 11, 13, 11, 14, -10, 11, -9, -3, 13, -5, -10, -4, -5]
  y_s = [0, 4,  11,  5, 11, 14,   7, 11,  4,  6,  5,  9,  12, 14, 14]
  z_s = [0, 1,  1,   1,  1,  1,  26,  1, 26, 26,  1, 26,  26, 26, 26]

  z_stack = [(0)]
  constraints = []
  for w, x_in, y_in, z_in in zip(range(0, 15), x_s, y_s, z_s):
    z_prev = z_stack[-1]
    if x_in > 10:
      z_stack.append(('w'+str(w), y_in))
    else:
      if z_in == 26:
        z_stack.pop()
      constraints.append((z_prev, x_in, 'w'+str(w)))
    # print(w, z_stack)
  for (z_prev, x_in, w_in) in constraints:
    print (z_prev, "%26", x_in, " = ", w_in)

  # Check a potential answer's stack at each iteration. 
  # for i in range(1, 15):
    # print(base_26(python_version([9, 2, 9, 1, 5, 9, 7, 9, 9, 9, 9, 4, 9, 8], slice=i)))


  #  assert_eq([int(c) for c in list("21611513911181")])

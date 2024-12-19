#!/usr/bin/env python3
import puzzle, re, copy

def parse_input(INPUT):
  return INPUT

class Intputer(object):
  (NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ, REL) = range(10)
  WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4, REL: 2}
  TERM = 99

  def __init__(self, instructions, inputs=[], id=""):
    self.program = list(map(int, instructions))
    self.saved_pc = 0
    self.saved_ram = copy.copy(self.program)
    self.saved_ram += [0] * 100000
    self.inputs = inputs
    self.last_output = None
    self.id = id
    self.relative_base = 0
    self.halted = False

  def get_a(self, modes, ram, pc):
    if modes[0] == 0:
      return ram[ram[pc+1]]
    elif modes[0] == 1:
      return ram[pc+1]
    elif modes[0] == 2:
      return ram[ram[pc+1]+self.relative_base]

  def get_a_addr(self, modes, ram, pc):
    if modes[0] == 0:
      return ram[pc+1]
    elif modes[0] == 1:
      # print("ERROR, INVALID IMMEDIATE MODE")
      return ram[pc+1]
    elif modes[0] == 2:
      return ram[pc+1]+self.relative_base

  def get_b(self, modes, ram, pc):
    # B is undefined, short circuit
    if len(modes) < 2: return None

    if modes[1] == 0:
      return ram[ram[pc+2]]
    elif modes[1] == 1:
      return ram[pc+2]
    elif modes[1] == 2:
      return ram[ram[pc+2]+self.relative_base]

  def get_c_addr(self, modes, ram, pc):
    # C is undefined, short circuit
    if len(modes) < 3: return None
    if modes[2] == 0:
      return ram[pc+3]
    elif modes[2] == 1:
      # print("ERROR, INVALID IMMEDIATE MODE")
      return ram[pc+3]
    elif modes[2] == 2:
      return ram[pc+3]+self.relative_base

  def out(self, *items):
    msg = ' '.join(map(str, items))
    if False:
      print(msg)

  def run(self):
    ram = self.saved_ram
    pc = self.saved_pc
    if self.saved_pc == -1:
      print("ERROR")
      return None, -1
    while ram[pc] != self.TERM:
      opcode, modes = self.process_instruction(ram[pc])
      width = self.WIDTHS[opcode]
      a=self.get_a(modes, ram, pc)
      a_addr=self.get_a_addr(modes, ram, pc)
      b=self.get_b(modes, ram, pc)
      c_addr=self.get_c_addr(modes, ram, pc)
      self.out(ram[pc], ram[pc+1:pc+width])
      if opcode == self.ADD:
        self.out("ADD modes a b out", modes, a, b, a+b, "to", c_addr)
        ram[c_addr] = a + b
      elif opcode == self.MUL:
        self.out("MUL modes a b out", modes, a, b, a*b, "to", c_addr)
        ram[c_addr] = a * b
      elif opcode == self.INPUT:
        self.out("INPUT", modes, "to", a_addr)
        if self.inputs:
          in_val = self.inputs.pop()
          ram[a_addr] = in_val
        else:
          self.saved_pc = pc
          self.saved_ram = ram
          return self.INPUT, None

      elif opcode == self.OUTPUT:
        self.out("OUTPUT", modes, a)
        self.saved_pc = pc + self.WIDTHS[opcode]
        self.saved_ram = ram
        self.last_output = a
        return self.OUTPUT, self.last_output

      elif opcode == self.JTR:
        self.out("JTR", modes, a, "to", b)
        if a != 0: 
          pc = b
          continue # needed because else pc gets incremented below
      elif opcode == self.JFAL:
        self.out("JFAL", modes, a, "to", b)
        if a == 0:
          pc = b
          continue # needed because else pc gets incremented below
      elif opcode == self.LT:
        self.out("LT", modes, a, b)
        if a < b: 
          ram[c_addr] = 1
        else: 
          ram[c_addr] = 0
      elif opcode == self.EQ:
        self.out("EQ", modes, a, b)
        if a == b: 
          ram[c_addr] = 1
        else:
          ram[c_addr] = 0
      elif opcode == self.REL:
        self.out("REL", modes, a)
        self.relative_base += a
      elif opcode == self.NULL:
        print("ERROR: NULL INSTRUCTION")
      else: 
        print("ERROR: GARBAGE INSTRUCTION")
      pc += self.WIDTHS[opcode]

    self.saved_pc = -1
    self.saved_ram = ram
    self.halted = True
    return self.TERM, None

  def process_instruction(self, inst):
    opcode = int(str(inst)[-2:])
    modes = []
    for c in str(inst)[-3::-1]:
      modes.append(int(c))
    while len(modes) < self.WIDTHS[opcode] - 1:
      modes.append(0)
    return opcode, modes

def one(INPUT):

  class RepairRobot(object):

    def __init__(self, instructions):
      self.puter = Intputer(instructions, [], id='a')
      self.floor = [[' ' for i in range(100)] for j in range(60)]
      self.loc = (40, 40)
      self.last_output = 1
      self.attempt = None
      self.final_loc = None

    def floor_get(self, loc):
      return self.floor[loc[0]][loc[1]]

    def next_input(self):

      if self.last_output == 2:
        # print("FOUND IT", self.loc)
        self.final_loc = self.loc

      # Process last output
      if self.attempt and self.last_output in [1, 2]:
        self.loc = self.loc[0] + self.attempt[0], self.loc[1] + self.attempt[1]
        self.floor[self.loc[0]][self.loc[1]] = '.'
      elif self.attempt:
        self.floor[self.loc[0] + self.attempt[0]][self.loc[1] + self.attempt[1]] = '#'

      DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
      walled = 0
      for i in range(4):
        d = DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) in ["#", "b"]:
          walled += 1
      if walled == 3:
        self.floor[self.loc[0]][self.loc[1]] = 'b'

      # Provide next input
      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) == " ":
          self.attempt = d
          return i + 1

      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) == ".":
          self.attempt = d
          return i + 1
      # print("NO INPUT")
      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        # print(self.floor_get(new_loc))


    def dump(self):
      floor = copy.deepcopy(self.floor)
      # floor[self.loc[0]][self.loc[1]] = 'D'
      # for l in floor:
      #   print(''.join(l))

    def run(self):
      for i in range(10000):
        code, out = self.puter.run()
        if code == Intputer.OUTPUT:
          # print("OUTPUT", out)
          self.last_output = out
          # print("**********")
        elif code == Intputer.INPUT: 
          next_ip = self.next_input()
          # print("INPUT", next_ip)
          self.puter.inputs.append(next_ip)
        else:
          # self.dump()
          # don't ask.
          self.floor[42][40] = 'b'
          break
    
    def pathfind(self):
      end = (28, 25)
      distances = {(40,40): 0}
      next_locs = [(40,40)]
      DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
      dist = 0
      idx = 0
      paths = {}
      while idx < len(next_locs):
        loc = next_locs[idx]
        idx += 1
        dist = distances[loc]
        for i in range(4):
          d = DIRS[i]
          new_loc = loc[0] + d[0], loc[1] + d[1]
          if self.floor_get(new_loc) == 'b':
            paths[new_loc] = loc
            next_locs.append(new_loc)
            if not new_loc in distances:
              distances[new_loc] = dist + 1
        self.floor[loc[0]][loc[1]] = 'm'
        self.dump()

      path = []
      node = end
      while node in paths:
        path.append(node)
        node = paths[node]
      # print(path)
      # print(len(path))
      return len(path) + 1 # todo +1
  rr=RepairRobot(INPUT[0].split(','))
  rr.run()
  rr.pathfind()

def two(INPUT):
  class RepairRobot(object):

    def __init__(self):
      self.puter = Intputer(INPUT[0].split(','), [], id='a')
      self.floor = [[' ' for i in range(100)] for j in range(60)]
      self.loc = (40, 40)
      self.last_output = 1
      self.attempt = None
      self.final_loc = None

    def floor_get(self, loc):
      return self.floor[loc[0]][loc[1]]

    def next_input(self):

      if self.last_output == 2:
        print("FOUND IT", self.loc)
        self.final_loc = self.loc

      # Process last output
      if self.attempt and self.last_output in [1, 2]:
        self.loc = self.loc[0] + self.attempt[0], self.loc[1] + self.attempt[1]
        self.floor[self.loc[0]][self.loc[1]] = '.'
      elif self.attempt:
        self.floor[self.loc[0] + self.attempt[0]][self.loc[1] + self.attempt[1]] = '#'

      DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
      walled = 0
      for i in range(4):
        d = DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) in ["#", "b"]:
          walled += 1
      if walled == 3:
        self.floor[self.loc[0]][self.loc[1]] = 'b'

      # Provide next input
      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) == " ":
          self.attempt = d
          return i + 1

      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if self.floor_get(new_loc) == ".":
          self.attempt = d
          return i + 1
      print("NO INPUT")
      for i in range(4):
        d=DIRS[i]
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        # print(self.floor_get(new_loc))


    def dump(self):
      floor = copy.deepcopy(self.floor)
      # floor[self.loc[0]][self.loc[1]] = 'D'
      for l in floor:
        print(''.join(l))

    def run(self):
      for i in range(10000):
        code, out = self.puter.run()
        if code == Intputer.OUTPUT:
          # print("OUTPUT", out)
          self.last_output = out
          # print("**********")
        elif code == Intputer.INPUT: 
          next_ip = self.next_input()
          # print("INPUT", next_ip)
          self.puter.inputs.append(next_ip)
        else:
          # self.dump()
          # don't ask.
          self.floor[42][40] = 'b'
          break
    
    def flood(self):
      start = (28, 25)
      locs = [start]
      next_locs = []
      n = 0
      while locs != []:
        n += 1
        for loc in locs:
          DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
          for i in range(4):
            d = DIRS[i]
            new_loc = loc[0] + d[0], loc[1] + d[1]
            if self.floor_get(new_loc) == 'b':
              next_locs.append(new_loc)
          self.floor[loc[0]][loc[1]] = 'O'
        locs = next_locs
        next_locs = []
      return n

  rr=RepairRobot()
  rr.run()
  return rr.flood()

p = puzzle.Puzzle("2019", "15")
p.run(one, 0)
p.run(two, 0)

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
  instructions = INPUT[0].split(',')

  class Grid(object):

    def __init__(self, width=50, height=50, grid=None):
      if grid:
        self.width = len(grid)
        self.height = len(grid[0])
        self.floor = grid
      else:
        self.floor = [[' ' for i in range(height)] for j in range(width)]
      
      self.overlay_pts = []

    def get(self, loc):
      if loc[0] >= len(self.floor) or loc[1] >= len(self.floor[0]) or loc[0] < 0 or loc[1] < 0:
        return '.'
      # print(loc, len(self.floor[loc[0]]))
      # print(self.floor[-1])
      return self.floor[loc[0]][loc[1]]

    def set(self, loc, val):
      self.floor[loc[0]][loc[1]] = val

    def __str__(self):
      floor = copy.deepcopy(self.floor)
      if self.overlay_pts:
        # print(self.overlay_pts[0])
        floor[self.overlay_pts[0][0][0]][self.overlay_pts[0][0][1]] = self.overlay_pts[0][1]
      rets = []
      for l in floor:
        rets.append(''.join(l))
      return '\n'.join(rets)

  class Bot(object):
    DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self, grid, loc):
      self.grid = grid
      self.loc = loc
      self.dir = self.DIRS[0]
      self.seen = [self.loc]
      self.seen_twice = []
      self.grid.overlay_pts = [[self.loc, 'B']]

    def legal_move(self, d):
      new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
      return self.grid.get(new_loc) == "#"

    def move(self, d):
      new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
      self.loc = new_loc
      if self.loc in self.seen:
        # print(self.loc, self.seen)
        self.seen_twice.append(self.loc)
        tot = 0
        for st in self.seen_twice:
          tot += st[0] * st[1]
        # print(tot)
        # print(self.seen_twice)
      self.seen.append(new_loc)
      self.dir = d
      self.grid.overlay_pts = [[self.loc, 'B']]

    def find_move(self):
      if self.legal_move(self.dir):
        self.move(self.dir)
        return
      for d in self.DIRS:
        new_loc = self.loc[0] + d[0], self.loc[1] + d[1]
        if new_loc in self.seen:
          continue
        if self.legal_move(d):
          self.move(d)
          return
      # print("ERROR: NO LEGAL MOVE")


  class ScaffoldRobot(object):

    def __init__(self):
      self.puter = Intputer(instructions, [], id='a')
      self.outputs = []


    def run(self):
      for i in range(10000):
        code, out = self.puter.run()
        if code == Intputer.OUTPUT:
          # print("OUTPUT", out)
          self.outputs.append(out)
        elif code == Intputer.INPUT: 
          next_ip = self.next_input()
          # print("INPUT", next_ip)
          self.puter.inputs.append(next_ip)
        else:
          break

      grid = []
      line = []
      bot = None
      for o in self.outputs:
        if o not in [35, 46, 10]:
          bot_loc = len(grid), len(line)
          line.append('#')
        elif o == 10:
          grid.append(line)
          line = []
        else:
          line.append(chr(o))
      # print('g', grid)
      # print('g-1', grid[-1])
      grid = grid[:-1]
      # Transpose grid https://www.geeksforgeeks.org/transpose-matrix-single-line-python/
      # z_grid = zip(*grid)
      # t_grid = []
      # for row in z_grid:
      # 	t_grid.append(row)
      g=Grid(grid=grid)	
      # print(g)
      b = Bot(g, bot_loc)
      for i in range(500):
        b.find_move()
        # print(g)
        # a=input()
      return b.seen_twice

  sr=ScaffoldRobot()
  st = sr.run()
  return sum([a*b for a, b in st])

def two(INPUT):
  instructions = INPUT[0].split(',')
  instructions[0] = 2
  class Grid(object):

    def __init__(self, width=50, height=50, grid=None):
      if grid:
        self.width = len(grid)
        self.height = len(grid[0])
        self.floor = grid
      else:
        self.floor = [[' ' for i in range(height)] for j in range(width)]
      
      self.overlay_pts = []

    def get(self, loc):
      if loc[0] >= len(self.floor) or loc[1] >= len(self.floor[0]) or loc[0] < 0 or loc[1] < 0:
        return '.'
      return self.floor[loc[0]][loc[1]]

    def set(self, loc, val):
      self.floor[loc[0]][loc[1]] = val

    def __str__(self):
      floor = copy.deepcopy(self.floor)
      if self.overlay_pts:
        print(self.overlay_pts[0])
        floor[self.overlay_pts[0][0][0]][self.overlay_pts[0][0][1]] = self.overlay_pts[0][1]
      rets = []
      for l in floor:
        rets.append(''.join(l))
      return '\n'.join(rets)

  #34 segments

  # Have to start with R12

  # have to end with 9, L, 9
  # has to be a 10, have to have a 6 next to a 10
  # 10, 10, 12 in order
  class ScaffoldRobot(object):

    def __init__(self):
      def process(instr):
        elems = []
        for item in instr.split(","):
          if elems:
            elems.append('44')
          for c in item:
            elems.append(str(ord(c)))
        return ','.join(elems)
      main_func ="A,B,A,C,B,C,B,C,A,C"
      move_a = "R,12,L,10,R,12"
      move_b = "L,8,R,10,R,6"
      move_c = "R,12,L,10,R,10,L,8"
      live_feed = "n"
      inputs = main_func, move_a, move_b, move_c, live_feed
      inputs = [process(lst) for lst in inputs]
      inputs = ",10,".join(inputs) + ",10"
      inputs = [int(a) for a in inputs.split(',')]
      inputs.reverse()
      self.puter = Intputer(instructions, inputs, id='a')
      self.outputs = []


    def run(self):
      for i in range(1000000):
        code, out = self.puter.run()
        if code == Intputer.OUTPUT:
          # print("OUTPUT", out)
          self.outputs.append(out)
        elif code == Intputer.INPUT: 
          # print("ERROR off input queue end")
          pass
        else:
          # print("?")
          break

  sr=ScaffoldRobot()
  sr.run()
  return sr.outputs[-1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "17")
  print(p.run(one, 0))
  print(p.run(two, 0))

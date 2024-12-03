import copy

class Intputer(object):
  (NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ, REL) = range(10)
  TERM = 99
  WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3,
           JFAL: 3, LT: 4, EQ: 4, REL: 2, TERM: 1}

  def __init__(self, instructions, inputs=[], id="", user_input=True, halt_on_output=False):
    self.program = list(map(int, instructions))
    self.pc = 0
    self.ram = copy.copy(self.program)
    self.ram += [0] * 100000
    self.user_input = user_input
    self.inputs = inputs
    self.outputs = []
    self.id = id
    self.relative_base = 0
    self.halted = False
    self.terminated = False

    # Hack for day 23.
    self.last_read = None
    # Hack for day 7
    self.halt_on_output = halt_on_output

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
      print(f'{msg}')

  def run(self):
    return self.run2()

  def run2(self):
    while not (self.halted or self.terminated):
      # print(f'pc: {self.pc}, data:{self.ram[self.pc]}')
      self.step()

  def step(self):  
    self.out(f'\n')
    self.out(f'id: {self.id}, pc: {self.pc}, inst: {self.ram[self.pc]}')
    opcode, modes = self.process_instruction(self.ram[self.pc])
    
    if opcode == self.TERM:
      self.terminated = True
      self.pc += self.WIDTHS[opcode]
      return

    width = self.WIDTHS[opcode]
    a = self.get_a(modes, self.ram, self.pc)
    a_addr = self.get_a_addr(modes, self.ram, self.pc)
    b = self.get_b(modes, self.ram, self.pc)
    c_addr = self.get_c_addr(modes, self.ram, self.pc)
    self.out(f'data:{self.ram[self.pc+1:self.pc+width]}')
    if opcode == self.ADD:
      self.out("ADD modes a b out", modes, a, b, a+b, "to", c_addr)
      self.ram[c_addr] = a + b
      # if a not in [0,1] and b not in [0,1]:
      #   print(f'ADD {a} {b}')
      self.pc += self.WIDTHS[opcode]
    elif opcode == self.MUL:
      self.out("MUL modes a b out", modes, a, b, a*b, "to", c_addr)
      self.ram[c_addr] = a * b
      self.pc += self.WIDTHS[opcode]
    elif opcode == self.INPUT:
      if self.inputs:
        in_val = self.inputs[0]
        self.inputs = self.inputs[1:]
        self.ram[a_addr] = in_val
        self.last_read = in_val
        self.pc += self.WIDTHS[opcode]
      elif self.user_input:
        in_val = list(map(ord, input()))
        self.ram[a_addr] = in_val[0]
        # self.last_read = in_val
        self.inputs = in_val[1:] + [10]
        self.pc += self.WIDTHS[opcode]
      else:
        self.out('HALT')
        self.halted = True
        return self.INPUT, None
      self.out("INPUT", in_val, "to", a_addr)
    elif opcode == self.OUTPUT:
      self.out("OUTPUT", modes, a)
      self.outputs.append(a)
      self.pc += self.WIDTHS[opcode]
      if self.halt_on_output == True:
        self.halted = True
    elif opcode == self.JTR:
      self.out("JTR", modes, a, "to", b)
      self.pc = b if a != 0 else self.pc + self.WIDTHS[opcode]
    elif opcode == self.JFAL:
      self.out("JFAL", modes, a, "to", b)
      self.pc = b if a == 0 else self.pc + self.WIDTHS[opcode]
    elif opcode == self.LT:
      self.out("LT", modes, a, b)
      if a < b: 
        self.ram[c_addr] = 1
      else: 
        self.ram[c_addr] = 0
      self.pc += self.WIDTHS[opcode]
    elif opcode == self.EQ:
      self.out("EQ", modes, a, b)
      if a == b: 
        self.ram[c_addr] = 1
      else:
        self.ram[c_addr] = 0
      self.pc += self.WIDTHS[opcode]
    elif opcode == self.REL:
      self.out("REL", modes, a)
      self.relative_base += a
      self.pc += self.WIDTHS[opcode]
    else: 
      print("ERROR: GARBAGE INSTRUCTION")

  def process_instruction(self, inst):
    opcode = int(str(inst)[-2:])
    modes = []
    if opcode == self.NULL:
      print("ERROR: NULL INSTRUCTION", inst, self.pc)
      raise ValueError
    for c in str(inst)[-3::-1]:
      modes.append(int(c))
    while len(modes) < self.WIDTHS[opcode] - 1:
      modes.append(0)
    return opcode, modes

#!/usr/bin/env python3
import puzzle

(NULL, ADD, MUL, INPUT, OUTPUT, JTR, JFAL, LT, EQ) = range(9)
WIDTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, JTR: 3, JFAL: 3, LT: 4, EQ: 4}
TERM = 99

def run(instring):
  ram = list(map(int, instring))
  ram += [0] * 400
  pc = 0
  outputs = []
  while ram[pc] != TERM:
    print(pc, ram[pc])
    opcode, modes = process_instruction(ram[pc])
    width = WIDTHS[opcode]
    a = 0
    b = 0
    if width > 2:
      a = ram[pc + 1] if modes[0] else ram[ram[pc + 1]] 
      b = ram[pc + 2] if modes[1] else ram[ram[pc + 2]] 

    if opcode == ADD:
      print("ADD", modes, ram[pc+1], ram[pc+2], ram[pc+3])
      print("ADD a b out", a, b, a+b)
      ram[ram[pc + 3]] = a + b
    elif opcode == MUL:
      print("MUL", modes, ram[pc+1], ram[pc+2], ram[pc+3])
      print("MUL a b out", a, b, a*b)
      ram[ram[pc + 3]] = a * b
    elif opcode == INPUT:
      print("INPUT", modes, ram[pc+1])
      in_val = int(input('input'))
      ram[ram[pc + 1]] = in_val
    elif opcode == OUTPUT:
      print("OUTPUT", modes, ram[pc+1])
      print("OUTPUT", ram[ram[pc + 1]])
      outputs.append(ram[ram[pc + 1]])
    elif opcode == JTR:
      print("JTR", a)
      if a != 0: 
        pc = b
        continue # needed because else pc gets incremented below
    elif opcode == JFAL:
      print("JFAL", a)
      if a == 0:
        pc = b
        continue # needed because else pc gets incremented below
    elif opcode == LT:
      print("LT", a, b)
      if a < b: 
        ram[ram[pc+3]] = 1
      else: 
        ram[ram[pc+3]] = 0
    elif opcode == EQ:
      print("EQ", a, b)
      if a == b: 
        ram[ram[pc+3]] = 1
      else:
        ram[ram[pc+3]] = 0
    elif opcode == NULL:
      pass
    
    pc += WIDTHS[opcode]
  return outputs

def process_instruction(inst):
  opcode = int(str(inst)[-2:])
  # print('oc, inst', opcode, inst)
  modes = []
  # busted?
  for c in str(inst)[-3::-1]:
    modes.append(int(c))
  while len(modes) < WIDTHS[opcode] - 1:
    modes.append(0)
  return opcode, modes

def one(INPUT):
  return run(INPUT[0].split(','))[-1]

def two(INPUT):
  return run(INPUT[0].split(','))[-1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "5")

  p.run(one, 0)
  p.run(two, 0)

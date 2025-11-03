#!/usr/bin/env python3
import puzzle
import re
from library import Grid
from rtree import index

def parse(INPUT):
  instrs = []
  for l in INPUT:
    if 'toggle' in l:
      instr = ['toggle']
    elif 'turn on' in l:
      instr = ['turn on']
    else:
      instr = ['turn off']
    match = re.findall(r'(\d+)', l)

    for m in match:
      instr.append(int(m))
    instrs.append(instr)
  return instrs

def regions(r1, r2):
  ax1, ay1, ax2, ay2 = r1
  bx1, by1, bx2, by2 = r2
  x_val = sorted(set([ax1, ax2, bx1, bx2]))
  y_val = sorted(set([ay1, ay2, by1, by2]))
  for x1, x2 in zip(x_val, x_val[1:]):
    for y1, y2 in zip(y_val, y_val[1:]):
      yield (x1, y1, x2, y2)

def within(r, pt):
  x, y = pt; rx1, ry1, rx2, ry2 = r
  return rx1 <= x < rx2 and ry1 <= y < ry2

def one(INPUT, two=False):
  instrs = parse(INPUT)
  if two: return

  idx = index.Index()
  idx.insert(0, (0,0,1000,1000), '0')
  next_id = 1
  for i, inst in enumerate(instrs):
    print("INST", inst)
    (op, overlay) = inst[0], inst[1:]
    # extend endpoints so rects have volume
    overlay[2] += 1; overlay[3] += 1
    bases = idx.intersection(overlay, objects=True)
    for base in bases:
      # print('overlapping base', base.bbox, base.object, overlay)
      idx.delete(base.id, base.bbox)
      segments = regions(base.bbox, overlay)
      for new_rect in segments:
        # print('nr', new_rect)
        new_ul = new_rect[0], new_rect[1]
        if within(base.bbox, new_ul):
          # if in both, add rect with value mutated
          if within(overlay, new_ul):
            if op == 'turn on':
              new_val = '1'
            elif op == 'turn off':
              new_val = '0'
            elif op == 'toggle':
              # print('TOGGLE')
              new_val = '1' if base.object == '0' else '0'
            # print('bonv', base.object, new_val)
            idx.insert(next_id, new_rect, obj = new_val)
            next_id += 1
          # if in base_rect and not in overlay, add rect with value stable
          else:
            idx.insert(next_id, new_rect, obj = base.object)
            next_id += 1

  on_lights = 0
  for obj in idx.intersection(idx.bounds, objects=True):
    x1, y1, x2, y2 = obj.bbox
    if obj.object == '1':
      # print("OUT", obj.bbox, obj.object)
      on_lights += (x2-x1)*(y2-y1)
  return int(on_lights)

def two(INPUT):
  return
  return one(INPUT, two=True)
  rows = defaultdict(list)
  instrs = parse(INPUT)
  for inst in instrs:
    (op, x1, y1, x2, y2) = inst
    for y in range(y1, y2+1):
      row_ops = rows[y]
      row_ops.append((op, x1, x2))
  on_lights = 0
  for y in range(1000):
    ops = rows[y]
    for x in range(1000):
      on = 0
      for op in ops:
        oper, x1, x2 = op
        if x1 <= x <= x2:
          if oper == "turn on":
            on += 1
          if oper == "turn off":
            on = max(on - 1, 0)
          if oper == "toggle":
            on += 2
      on_lights += on
  print(on_lights)
  return on_lights

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "6")

  p.run(one, 0)
  p.run(two, 0)

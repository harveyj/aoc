#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  beacon_sensors = []
  for l in INPUT:
     m = re.match(r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)", l)
     if m:
       s_x, s_y, b_x, b_y = list(map(int, m.group(1, 2, 3, 4)))
       manhattan = abs(s_x - b_x) + abs(s_y - b_y)
       beacon_sensors.append((s_x, s_y, b_x, b_y, manhattan))
  return beacon_sensors

def target_row(beacon_sensors, target_y):
  ret = []
  for s_x, s_y, b_x, b_y, manhattan in beacon_sensors:
    y_delt = abs(s_y - target_y)
    range_width = max(0, manhattan - y_delt)
    excluded_range = s_x - range_width, s_x + range_width
    ret.append(excluded_range)
  return ret

def one(INPUT):
  beacon_sensors = parse(INPUT)
  ranges = target_row(beacon_sensors, 2000000)
  excluded = set()
  for s, e in ranges:
    while s < e:
      excluded.add(s)
      s+= 1
  return len(excluded)

def check_point(beacon_sensors, pt):
  x, y = pt
  for s_x, s_y, b_x, b_y, manhattan in beacon_sensors:
    if abs(s_x - x) + abs(s_y - y) <= manhattan:
      return True
  return False

def two(INPUT):
  beacon_sensors = parse(INPUT)
  MAX = 4000000
  for s_x, s_y, b_x, b_y, manhattan in beacon_sensors:
    # dx, dy, offset_x, offset_y
    iters = [[1, 1, -manhattan-1, 0], [1, -1, -manhattan-1, 0], [-1, 1, manhattan+1, 0], [-1, -1, manhattan+1, 0]]
    for dx, dy, offset_x, offset_y in iters:
      x, y = s_x + offset_x, s_y+offset_y
      for i in range(manhattan+1):
        x += dx; y += dy
        if x < 0 or x > MAX or y < 0 or y > MAX:
          continue
        if not check_point(beacon_sensors, (x, y)):
          return x * 4000000 + y

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "15")

  p.run(one, 0) 
  p.run(two, 0) 
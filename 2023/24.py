#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  def parse_line(l):
    left, right = l.split('@')
    return list(map(int, left.split(','))), list(map(int, right.split(',')))
  return [parse_line(l) for l in INPUT]

def mb(line):
  x, y, z = line[0]; dx, dy, dz = line[1]
  m = dy/dx
  b = y - x * m
  return m, b

def intersect(m_1, b_1, m_2, b_2):
  x = (b_2 - b_1) / (m_1 - m_2)
  y = m_1 * x + b_1
  return (x, y)

def intersect_time(dx, x_0, x_int):
  return (x_int - x_0) / dx

def evaluate(line, t):
  x, y, z = line[0]; dx, dy, dz = line[1]
  return x + t * dx, y + t * dy, z + t * dz 

def one(INPUT):
  invals = parse_input(INPUT)
  x_min, x_max = 200000000000000, 400000000000000
  y_min, y_max = 200000000000000, 400000000000000
  out = 0
  for i, line1 in enumerate(invals):
    m_1, b_1 = mb(line1)
    for line2 in invals[i+1:]:
      m_2, b_2 = mb(line2)
      if m_1 == m_2: 
        # print('***')
        # print('parallel', line1, line2)
      else:
        # print('***')
        x_int, y_int = intersect(m_1, b_1, m_2, b_2)
        time_1 = intersect_time(line1[1][0], line1[0][0], x_int)
        if time_1 < 0: print('past for A')
        time_2 = intersect_time(line2[1][0], line2[0][0], x_int)
        if time_2 < 0: print('past for B')
        # print('A, B', line1, line2, x_int, y_int)
        if x_min < x_int < x_max and y_min < y_int < y_max and time_1 > 0 and time_2 > 0:
          out += 1
  return out

def make_line(pt1, pt2):
  slope = (a - b for a, b in zip(pt1, pt2))
  return pt1, slope

import scipy, numpy as np

def iter(line1, line2, line3):
  x0, y0, z0, dx0, dy0, dz0 = line1[0] + line1[1]
  x1, y1, z1, dx1, dy1, dz1 = line2[0] + line2[1]
  x2, y2, z2, dx2, dy2, dz2 = line3[0] + line3[1]
  
  # xa, dxa, ya, dya, za, dza, t0, t1, t2
  def func(x):
    xa, dxa, ya, dya, za, dza, t0, t1, t2 = x
    return [x0+dx0*t0 - xa - dxa*t0,
            y0+dy0*t0 - ya - dya*t0,
            z0+dz0*t0 - za - dza*t0,
            x1+dx1*t1 - xa - dxa*t1,
            y1+dy1*t1 - ya - dya*t1,
            z1+dz1*t1 - za - dza*t1,
            x2+dx2*t2 - xa - dxa*t2,
            y2+dy2*t2 - ya - dya*t2,
            z2+dz2*t2 - za - dza*t2,
            ]
  # xa, dxa, ya, dya, za, dza
  def func2(x):
    xa, dxa, ya, dya, za, dza = x
    return [(x0-xa)/(dxa-dx0) - (y0-ya)/(dya-dy0),
            (y0-ya)/(dya-dy0) - (z0-za)/(dza-dz0),
            (x1-xa)/(dxa-dx1) - (y1-ya)/(dya-dy1),
            (y1-ya)/(dya-dy1) - (z1-za)/(dza-dz1),
            (x2-xa)/(dxa-dx2) - (y2-ya)/(dya-dy2),
            (y2-ya)/(dya-dy2) - (z2-za)/(dza-dz2),
            ]

  for i in range(1000):
    vect = scipy.optimize.fsolve(func2, np.random.rand(6), xtol=0.000000000001, maxfev=1000)
    xa, dxa, ya, dya, za, dza = vect
    if sum(map(abs, func2(vect))) < 0.00000001:
      # print(func2(vect))
      # print('start', xa, ya, za)
      # print('velo', dxa, dya, dza)
      answer = round(xa) + round(ya) + round(za)
      return answer
  return None

def two(INPUT):
  invals = parse_input(INPUT)
  for i in range(len(invals) - 2):
    print(iter(invals[i], invals[i+1], invals[i+2]))

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "24")

  p.run(one, 0) 
  p.run(two, 0) 

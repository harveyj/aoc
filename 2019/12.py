#!/usr/bin/env python3
import puzzle, re, math

def parse_input(INPUT):
  return INPUT

class Moon(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.vx = 0
    self.vy = 0
    self.vz = 0

  def __str__(self):
    return "pos=<x=%3i, y=%3i, z=%3i>, vel=<x=%3i, y=%3i, z=%3i>" % (self.x, self.y, self.z, self.vx, self.vy, self.vz)

  def gravity(self, moons):
    for m in moons:
      if self == m: continue
      if self.x > m.x: self.vx -= 1
      elif self.x < m.x: self.vx += 1
      if self.y > m.y: self.vy -= 1
      elif self.y < m.y: self.vy += 1
      if self.z > m.z: self.vz -= 1
      elif self.z < m.z: self.vz += 1

  def velocity(self):
    self.x += self.vx
    self.y += self.vy
    self.z += self.vz


def one(INPUT):
  lines = INPUT
  pat = "<x=(.*), y=(.*), z=(.*)>"
  regex = re.compile(pat)
  moons=[]
  for l in lines:
    mat = re.match(regex, l)
    if mat:
      x, y, z = map(int, mat.group(1,2,3))
      moons.append(Moon(x, y, z))

  for i in range(1001):
    print("After %i steps" % i)
    for m in moons:
      print(m)
    nrg = 0
    for m in moons:
      nrg += (abs(m.x) + abs(m.y) + abs(m.z)) * (abs(m.vx) + abs(m.vy) + abs(m.vz))
    for m in moons:
      m.gravity(moons)
    for m in moons:
      m.velocity()

  return nrg

# TODO clean up more copypasta
def two(INPUT):
  lines=INPUT
  pat = "<x=(.*), y=(.*), z=(.*)>"
  regex = re.compile(pat)
  moons=[]
  start_moons = []
  for l in lines:
    mat = re.match(regex, l)
    if mat:
      x, y, z = map(int, mat.group(1,2,3))
      moons.append(Moon(x, y, z))
      start_moons.append(Moon(x, y, z))

  xs = {}
  ys = {}
  zs = {}
  for i in range(1000000):
    for m in moons:
      m.gravity(moons)
    for m in moons:
      m.velocity()

    all_x = tuple([(m.x, m.vx) for m in moons])
    all_y = tuple([(m.y, m.vy) for m in moons])
    all_z = tuple([(m.z, m.vz) for m in moons])
    
    last_x = xs.get(all_x, 100000000)
    x_period = i - last_x
    xs[all_x] = i
    # print(x_period, all_x)

    last_y = ys.get(all_y, 100000000)
    y_period = i - last_y
    ys[all_y] = i
    # print(y_period, all_y)

    last_z = zs.get(all_z, 100000000)
    z_period = i - last_z
    zs[all_z] = i
    # print(z_period, all_z)

    if x_period > 0 and y_period > 0 and z_period > 0:
      return math.lcm(x_period, y_period, z_period)

if __name__ != '__main':
  p = puzzle.Puzzle("2019", "12")
  print(p.run(one, 0))
  print(p.run(two, 0))

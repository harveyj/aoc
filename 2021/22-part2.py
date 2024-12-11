import input22, re
import itertools
from functools import partial

# TEST4=26
# TEST2 = TEST with a few moved pieces
INPUT=input22.INPUT_TEST2
X, Y, Z = range(3)

def lower_left_in(cube1, pt):
  c11, c12 = cube1
  x_int = c11[X] <= pt[X] < c12[X]
  y_int = c11[Y] <= pt[Y] < c12[Y] 
  z_int = c11[Z] <= pt[Z] < c12[Z] 
  return x_int and y_int and z_int

def parse_cube(l):
  match = re.search("(.*) .=(.*)\.\.(.*),.=(.*)\.\.(.*),.=(.*)\.\.(.*)", l) #"
  new_is_on = match.group(1) == 'on'
  x1, x2, y1, y2, z1, z2 = tuple(map(int, match.group(2, 3, 4, 5, 6, 7)))
  new_cube = ((x1, y1, z1), (x2+1, y2+1, z2+1))
  return new_is_on, new_cube

cubes = []
all_x, all_y, all_z = [], [], []
for l in INPUT:
  cube_is_on, cube = parse_cube(l)
  cubes.append((cube_is_on, cube))  
  all_x.extend((cube[0][X], cube[1][X]))
  all_y.extend((cube[0][Y], cube[1][Y]))
  all_z.extend((cube[0][Z], cube[1][Z]))

all_x = sorted(all_x)
all_y = sorted(all_y)
all_z = sorted(all_z)
cubes.reverse()

print(cubes)
tot = 0
for z1, z2 in zip(all_z, all_z[1:]):
  print('')
  cubes_zf = [(cube_on, cube) for (cube_on, cube) in cubes if cube[0][Z] <= z1 < cube[1][Z]]
  # print('zf',z1, z2, list(cubes_zf))

  for y1, y2 in zip(all_y, all_y[1:]):
    print('.',end="")
    cubes_yf = [(cube_on, cube) for (cube_on, cube) in cubes if cube[0][Y] <= y1 < cube[1][Y]]
    # print('yf',y1, y2, list(cubes_zf))

    for x1, x2 in zip(all_x, all_x[1:]):
      if next((cube_on for cube_on, cube in cubes_yf if lower_left_in(cube, (x1, y1, z1))), False):
        # print('adding', (x1, x2), (y1, y2), (z1, z2))
        tot += (x2 - x1) * (y2 - y1) * (z2 - z1)
print(tot)
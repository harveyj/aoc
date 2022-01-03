from collections import defaultdict

# Part 1
def apex_y(v_x, v_y):
  return v_y*(v_y+1) / 2
def apex_x(v_x, v_y):
  if v_x > v_y:
    delt = v_x - v_y
    return v_x*(v_x+1)//2 - delt*(delt+1)//2
  else:
    return v_x*(v_x+1)//2 

# print(apex_x(6,9))
# print(apex_y(6,9))
# print(apex_y(6,3))

# adding one to y brings the apex up by y
# a number in the sum of y needs to fall between apex_y - base_y_1, apex_y - base_y_2

def find_legal_y(base_y_1, base_y_2, base_x_1, base_x_2):
  max_v_y = -1
  for v_y_0 in range(1000):
    a_y = apex_y(0, v_y_0)
    y_l = a_y - base_y_1
    y_h = a_y - base_y_2
    max_y = -1
    for y in range(500):
      if y_l <= y*(y+1)/2 <= y_h:
        max_v_y = v_y_0
  for v_y_0 in range(max_v_y, 0, -1):
    for v_x_0 in range(200):
      for t in range(200):
        d = v_x_0 - t
        x_t = v_x_0 * (v_x_0 + 1) / 2 - d*(d+1)/2
        if base_x_1 < x_t < base_x_2:
          return v_x_0, max_v_y
  return -1

v_x, v_y = find_legal_y(-5, -10, 20, 30)
v_x, v_y = find_legal_y(-186, -215, 34, 67)
print("vx vy", v_x, v_y, apex_y(0, v_y))
x=0
y=0
for i in range(250):
  x += v_x
  y += v_y
  v_x -= 1
  v_y -= 1
  if v_x < 0:
    v_x = 0
  # print(i, x, y)

### Part 2


def is_legal(v_x_0, v_y_0, base_x_1, base_x_2,base_y_1, base_y_2):
  x=0
  y=0
  v_x = v_x_0
  v_y = v_y_0
  for i in range(50):
    x += v_x
    y += v_y
    v_x -= 1
    v_y -= 1
    if v_x < 0:
      v_x = 0
    if base_x_1 <= x <= base_x_2 and base_y_1 <= y <= base_y_2:
      return True
  return False

def find_all_legal_y(base_x_1, base_x_2, base_y_1, base_y_2):

  max_v_y = -1
  for v_y_0 in range(4000):
    a_y = apex_y(0, v_y_0)
    y_l = a_y - base_y_2
    y_h = a_y - base_y_1
    max_y = -1
    for y in range(600):
      if y_l <= y*(y+1)/2 <= y_h:
        max_v_y = v_y_0
        break
  for v_y_0 in range(-20*max_v_y, max_v_y+1):
    for v_x_0 in range(-500, 500):
        if is_legal(v_x_0, v_y_0, base_x_1, base_x_2, base_y_1, base_y_2):
          yield v_x_0, v_y_0

# for i in find_all_legal_y(-186, -215, 34, 67):
#   print(i)

# print(find_all_legal_y(-5, -10, 20, 30))
# print(is_legal(6, 9,20, 30, -10, -5))
print((1 for _ in find_all_legal_y(20, 30, -10, -5)))
all_test = find_all_legal_y(20, 30, -10, -5)
print(len(list(all_test)))
print(sum(1 for _ in find_all_legal_y(34, 67, -215, -186)))

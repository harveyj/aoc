
# Part 1
def apex_y(v_x, v_y):
  return v_y*(v_y+1) / 2

def find_all_legal_y(base_y_1, base_y_2):
  for v_y_0 in range(-100000, 100000):
    v_y = v_y_0
    y=0
    for t in range(1000):
      if base_y_1 <= y <= base_y_2:
        yield v_y_0, y, t
      y += v_y
      v_y -= 1

def find_legal_x_for_y(base_x_1, base_x_2, base_y_1, base_y_2, v_y_0, t):
  for v_x_0 in range(1500):
    if v_x_0 > t:
      x_d = v_x_0 - t
      x = v_x_0 *(v_x_0+1) // 2 - x_d * (x_d + 1) //2
    else:
      x = v_x_0 *(v_x_0+1) // 2
    if base_x_1 <= x <= base_x_2:
      yield v_x_0, v_y_0


# for i in find_all_legal_y(-186, -215, 34, 67):
#   print(i)

# print(find_all_legal_y(-5, -10, 20, 30))
# print(is_legal(6, 9,20, 30, -10, -5))
base_x_1, base_x_2, base_y_1, base_y_2 = 20, 30, -10, -5
base_x_1, base_x_2, base_y_1, base_y_2 = 34, 67, -215, -186
all_ys = find_all_legal_y(base_y_1, base_y_2)
all_ys_set=set(all_ys)
all = set()
for v_y_0, y, t in all_ys_set:
  # print(v_y_0, y, t)
  all.update(find_legal_x_for_y(base_x_1, base_x_2, base_y_1, base_y_2, v_y_0, t))
print(all, len(all))
# all_full = find_all_legal_y(34, 67, -215, -186)
# all_full_l = list(all_full)
# print(all_full_l)
# print(len(all_full_l))


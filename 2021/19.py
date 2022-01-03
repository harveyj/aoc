import input19, copy
from collections import *

in_segs = input19.INSTR_EASY.split("\n\n")
in_segs = input19.INSTR_TEST.split("\n\n")
# in_segs = input19.INSTR_FULL.split("\n\n")

def rotate(x, y, z, i):
  return [
  [ x,  y,  z],
  [-y,  x,  z],
  [-x, -y,  z],
  [ y, -x,  z],
  
  [ x, -y, -z],
  [ y,  x, -z],
  [-x,  y, -z],
  [-y, -x, -z],
  
  [ x,  z, -y],
  [-y,  z, -x],
  [-x,  z,  y],
  [ y,  z,  x],

  [ y, -z, -x],
  [-x, -z, -y],
  [-y, -z,  x],
  [ x, -z,  y],
  
  [ z,  y, -x],
  [ z, -x, -y],
  [ z, -y,  x],
  [ z,  x,  y],
  
  [-z,  x, -y],
  [-z, -y, -x],
  [-z, -x,  y],
  [-z,  y,  x]][i]

class Scan:
  def __init__(self):
    self.pts = []

def translate_pts(pts, pt1, pt2, i):
  new_pts = set()
  new_pt2 = rotate(*pt2, i)
  offset = tuple(xyz_1 - xyz_2 for xyz_1, xyz_2 in zip(pt1, new_pt2))
  # print(offset)
  for my_pt in pts:
    my_pt = rotate(*my_pt, i)
    new_pt = add(my_pt, offset)
    new_pts.add(new_pt)
  return offset, new_pts

def add(p1, p2):
  return tuple(xyz + o_xyz for xyz, o_xyz in zip(p1, p2))

def match(scan1pts, scan2pts):
  for pt1 in scan1pts:
    for pt2 in scan2pts:
      for i in range(24):
        offset, new_pts = translate_pts(scan2pts, pt1, pt2, i)
        intersect = set(new_pts).intersection(set(scan1pts))
        l = len(intersect)
        if l >= 12:
          return offset, i, new_pts
  return None, -1, []

# scans = []
# for i, seg in enumerate(in_segs):
#   scan = Scan()
#   for l in seg.split('\n')[1:]:
#     scan.pts.append(tuple(map(int, l.split(","))))
#   scans.append(scan)


# connections = defaultdict(list)
# for i, scan1 in enumerate(scans):
#   for j, scan2 in enumerate(scans):
#     if i != j:
#       offset, m_val, new_pts = match(scan1.pts, scan2.pts)
#       if m_val != -1:
#         connections[i].append((j))
#         print(i, j)

# # connections = {0: [1], 1: [0, 3, 4], 2: [4], 3: [1], 4: [1, 2]}
# offsets_zero = {0: (0,0,0)}
# queue = deque([(0, scans[0].pts)])
# all_pts = set(scans[0].pts)
# while len(queue) > 0:
#   key, pts = queue.pop()
#   for new_key in connections[key]:
#     new_offset, _, new_pts = match(pts, scans[new_key].pts)
#     if new_key not in offsets_zero:
#       offsets_zero[new_key] = new_offset
#       queue.append((new_key, new_pts))
#       all_pts.update(new_pts)
#       print(new_pts)
# print(len(all_pts))
# print(offsets_zero)

# Computation takes a long time so short circuit it, as you only need the orientations and offsets.
TEST = {0: (0, 0, 0), 1: (68, -1246, -43), 3: (-92, -2380, -20), 4: (-20, -1133, 1061), 2: (1105, -1205, 1229)}
FULL = {0: (0, 0, 0), 15: (-34, -39, -1212), 19: (-23, -18, 1148), 3: (-16, 29, 2262), 1: (1276, -97, -1275), 23: (-1232, 18, -1286), 2: (-2296, -97, -1318), 4: (-1152, 1250, -1236), 10: (-1185, -91, -2525), 9: (-2361, 82, -2400), 5: (-2394, 32, -3766), 18: (-2426, 1264, -2514), 13: (-2354, 1125, -3678), 20: (-2341, 1264, -1211), 24: (-3477, 1147, -2567), 11: (-2457, -48, -4796), 12: (-2413, -1237, -3623), 22: (-3623, 9, -3737), 17: (-2424, -1251, -1267), 7: (-3490, -1240, -1188), 21: (-2307, -2338, -1261), 25: (-2306, -1164, 24), 6: (-1164, -1250, 15), 16: (-2316, -2427, 3), 8: (-3651, -2454, 15), 14: (-3533, -3667, -159)}

dists = []
for k1, v1 in FULL.items():
  for k2, v2 in FULL.items():
    dist = abs(v1[0] - v2[0]) +     abs(v1[1] - v2[1]) +     abs(v1[2] - v2[2]) 
    # print(dist)
    dists.append(dist)
print(max(dists))

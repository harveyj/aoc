#!/usr/bin/env python3

from collections import *
import puzzle
import numpy as np
import itertools

def ptpt_vectors(scan):
  return scan[None, :, :] - scan[:, None, :]

def intersection(a, b):
  rows, cols = a.shape
  dt = {'names':['f{}'.format(i) for i in range(cols)],
         'formats':cols * [a.dtype]}

  intersect = np.intersect1d(a.view(dt), b.view(dt))
  return intersect.view(a.dtype).reshape(-1, a.shape[1])

def axis_swaps():
  for perm in itertools.permutations(range(3)):
    mat = np.zeros([3,3], dtype=int)
    for y, target_x in enumerate(perm):
      mat[target_x, y] = 1
    if np.linalg.det(mat) == 1:
      yield mat 


def rotations():
  for perm in itertools.permutations(range(3)):
    # perm is the x location of the value in each row
    for sign_set in itertools.product([-1, 1], repeat=3):
      mat = np.zeros([3,3], dtype=int)
      for y, target_x in enumerate(perm):
        mat[target_x, y] = sign_set[y]
      if np.linalg.det(mat) == 1:
        yield mat 

def one(INPUT, two=False):
  scans = []
  for i, seg in enumerate('\n'.join(INPUT).split('\n\n')):
    pts = []
    for l in seg.split('\n')[1:]:
      pts.append(tuple(map(int, l.split(","))))
    scan = np.array(pts)
    scans.append(scan)

  # find the vectors between all pairs of points in each scan
  vectors = [ptpt_vectors(s) for s in scans]
  vectors_flat = [v.reshape(-1, v.shape[-1]) for v in vectors]
  vectors_rot = [[vf @ rot for rot in rotations()] for vf in vectors_flat]
  overlaps = defaultdict(list)
  for i in range(len(scans)):
    for j in range(len(scans)):
      if i == j: continue
      for r_idx in range(24):
        vectors_a_flat = vectors_flat[i]
        vectors_b_rot = vectors_rot[j][r_idx]
        inter_a_b = intersection(vectors_a_flat, vectors_b_rot)
        # if there are 12 points that have at least 11 vectors in common (22 given double-counting)
        # that means those 12 points overlap, AND are strongly connected and you know the orientation
        if inter_a_b.shape[0] > 100:
          overlaps[i] += ((j, r_idx),)

  offsets = {0:np.zeros((3,))}
  oriented_scans = {0: scans[0]}
  queue = [0]

  def find_intersection(base, new_rot):
    for pt_base in base:
      for pt_rot in new_rot:
        delta = pt_rot - pt_base
        if len(intersection(base, new_rot - delta)) >= 12:
          return delta
    return None

  while queue:
    # invariant: base_idx is in oriented_scans and properly offset
    # maintain invariant via bfs
    base_idx = queue.pop(0)
    base = oriented_scans[base_idx]
    for item in overlaps[base_idx]:
      tgt_idx, _ = item
      # TODO don't need to iter over all rotations 
      for rot in rotations():
        if tgt_idx in oriented_scans.keys(): continue
        queue.append(tgt_idx)
        # find the offset (x, y, z) you can adjust b with such that > 12 points overlap
        # this is some b_pt - a_pt
        new_rot = scans[tgt_idx] @ rot
        delta = find_intersection(base, new_rot)
        if not delta is None:
          oriented_scans[tgt_idx] = new_rot - delta
          offsets[tgt_idx] = - delta
  all_pts = set()
  for scan in oriented_scans.values():
    pts_immut = set(map(tuple, scan))
    all_pts |= set(pts_immut)
  if two:
    return max([np.sum(np.abs(a - b)) for a in offsets.values() for b in offsets.values()])
  else:
    return len(all_pts)


def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "19")

  # print(p.run(one, 0))
  print(p.run(two, 0))

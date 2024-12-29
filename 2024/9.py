#!/usr/bin/env python3
import puzzle, copy
from itertools import accumulate
import bisect
from collections import deque, defaultdict
from sortedcontainers import SortedList
import itertools

def parse_input(INPUT):
  return list(map(int, INPUT))

def process(blocks, skips):
  fills = []
  skips = copy.copy(skips)
  for bid, b_size in list(blocks)[-1::-1]:
    for i in range(b_size):
      fills.append(bid)
      if skips[0] == 0: skips.pop(0)
      if not skips: 
        return fills
      skips[0] -= 1
  return fills

def checksum(out):
  return sum([a*int(b) for a, b in enumerate(out) if b != '.'])

def one(INPUT):
  items = parse_input(INPUT[0])
  blocks = list(enumerate(items[::2]))
  total = sum(items[::2])
  skips = items[1::2]
  fills = process(blocks, skips)
  fills_idx = 0
  out = []
  for block, skip in zip(blocks, skips):
    bid, bsize = block
    for i in range(bsize):
      if len(out) == total:
        return checksum(out)
      out += [bid]
    for i in range(skip):
      if len(out) == total:
        return checksum(out)
      out.append(fills[fills_idx])
      fills_idx += 1

def checksum2(out):
  ret = 0
  idx = 0
  for a, b in out:
    for i in range(b):
      if a != '.':
        ret += a * idx
      idx += 1
  return ret

def two_slow(INPUT):
  items = parse_input(INPUT[0])
  array = [[i//2 if i % 2 == 0 else '.', size] for i, size in enumerate(items)]
  id = len(items)//2
  while id > -1:
    from_idx = 0
    # scan forward to find start of id block
    while from_idx < len(array):
      if array[from_idx][0] == id:
        break
      from_idx += 1
    to_idx = 0
    # scan forward finding where the empty span is that fits it
    while to_idx < from_idx:
      if array[to_idx][0] == '.' and array[to_idx][1] >= array[from_idx][1]:
        array[to_idx][1] -= array[from_idx][1]
        array.insert(to_idx, copy.copy(array[from_idx]))
        array[from_idx+1][0] = '.'
        break
      to_idx += 1
    # consolidate any empty spans
    idx = 0
    while idx < len(array) - 1:
      if array[idx][0] == '.' and array[idx+1] == '.':
        array[idx][1] += array[idx+1][1]
        del array[idx+1]
        continue
      idx += 1
    id -= 1
  return checksum2(array)

def render(blocks, gaps):
  gaps = [(gap_idx, '.', gap_span) for gap_idx, gap_span in gaps]
  combined = sorted(blocks + gaps, key=lambda a: a[0])
  return ''.join([str(id)*span for _, id, span in combined])

def checksum3(blocks):
  ret = 0
  for start_idx, id, span in blocks:
    for i in range(span):
      ret += (start_idx + i) * id
  return ret


def one_fast(INPUT):
  items = parse_input(INPUT[0])
  # start_idx, span
  indices = list(zip([0]+list(accumulate(items)), items))
  blocks = SortedList([(start_idx, id, span) for (id, (start_idx, span)) in enumerate(indices[0::2])])
  gaps = deque([(start_idx, span) for (_, (start_idx, span)) in enumerate(indices[1::2])])
  for block_idx, block_id, block_span in blocks[::-1]:
    if not gaps or gaps[0][0] > block_idx:
      break
    while block_span > 0:
      gap_idx, gap_span = gaps.popleft()
      if gap_idx > block_idx:
        blocks[-1] = (block_idx, block_id, block_span)
        break
      # up to block span or gap span
      consumed = min(block_span, gap_span)
      if consumed == block_span: blocks.pop()
      block_span = block_span - consumed
      bisect.insort(blocks, (gap_idx, block_id, consumed))
      if gap_span > consumed:
        gaps.appendleft((gap_idx + consumed, gap_span - consumed))

  return checksum3(blocks)

def two_fast(INPUT):
  items = parse_input(INPUT[0])
  # start_idx, span
  indices = list(zip([0]+list(accumulate(items)), items))
  blocks = [(start_idx, id, span) for (id, (start_idx, span)) in enumerate(indices[0::2])]
  gaps = deque([(start_idx, span) for (_, (start_idx, span)) in enumerate(indices[1::2])])
  i = len(blocks) - 1
  while i > 0:
    block_idx, block_id, block_span = blocks[i]
    j = 0
    while j < len(gaps) and gaps[j][0] < block_idx:
      gap_idx, gap_span = gaps[j]
      # print(f'considering {block_idx} {block_id}, {block_span} {gap_idx} {gap_span}')
      if block_span <= gap_span:
        del gaps[j]
        del blocks[i]
        i += 1
        bisect.insort(blocks, (gap_idx, block_id, block_span))
        bisect.insort(gaps, (gap_idx+block_span, gap_span - block_span))
        idx = bisect.bisect_left(gaps, (block_idx, block_span))
        new_idx = block_idx; new_span = block_span
        gap_left = gaps[idx-1]
        gap_right = gaps[idx] if idx < len(gaps) else None
        # if previous gap abuts new gap
        if gap_left[0] + gap_left[1] == block_idx:
          # print('expanding left')
          new_idx = gap_left[0]
          new_span += gap_left[1]
          gaps.remove(gap_left)
        # if following gap abuts new gap
        if gap_right and block_idx + block_span == gap_right[0]:
          # print('expanding rt')
          new_span += gap_right[1]
          gaps.remove(gap_right)
        bisect.insort(gaps, (new_idx, new_span))
        break
      j += 1
    # print('after', i, render(blocks, gaps))
    i -= 1

  return checksum3(blocks)

def find_left(gaps_dict, block_idx):
  indexes = {i: gaps_dict[i].bisect_left((block_idx, -1)) for i in range(1, 500)}
  entries = [gaps_dict[i][indexes[i]] for i in range(1, 500) if indexes[i] < len(gaps_dict[i])]
  entries = sorted(entries)
  return entries[-1] if entries else None

def find_right(gaps_dict, block_idx):
  indexes = {i: gaps_dict[i].bisect_right((block_idx, -1)) for i in range(1, 500)}
  entries = [gaps_dict[i][indexes[i]] for i in range(1, 500) if indexes[i] < len(gaps_dict[i])]
  entries = sorted(entries)
  return entries[0] if entries else None

def two_faster(INPUT):
  items = parse_input(INPUT[0])
  # start_idx, span
  indices = list(zip([0]+list(accumulate(items)), items))
  blocks = [(start_idx, id, span) for (id, (start_idx, span)) in enumerate(indices[0::2])]
  gaps_in = deque([(start_idx, span) for (_, (start_idx, span)) in enumerate(indices[1::2])])
  gaps_dict = {i:SortedList([g for g in gaps_in if g[1] == i]) for i in range(1, 500)}
  i = len(blocks) - 1
  seen = set()
  while i > 0:
    block_idx, block_id, block_span = blocks[i]
    # take all first entries of gaps_dict where block_span <= i, sort by location, first location is winner
    all_feasible_gaps = sorted([gaps_list[0] for (gap_size, gaps_list) in gaps_dict.items() if gap_size >= block_span and gaps_list and gaps_list[0][0] < block_idx])
    if not all_feasible_gaps or block_id in seen: 
      i -= 1
      continue
    seen.add(block_id)
    gap_idx, gap_span = all_feasible_gaps[0]
    gaps_dict[gap_span].remove((gap_idx, gap_span))
    del blocks[i]
    bisect.insort(blocks, (gap_idx, block_id, block_span))
    remaining = gap_span - block_span
    if remaining != 0: 
      gaps_dict[remaining].add((gap_idx+block_span, remaining))

    new_idx = block_idx; new_span = block_span
    gap_left = find_left(gaps_dict, block_idx)
    gap_right = find_right(gaps_dict, block_idx)
    # if previous gap abuts new gap
    if gap_left and (gap_left[0] + gap_left[1] == block_idx):
      new_idx = gap_left[0]
      new_span += gap_left[1]
      gaps_dict[gap_left[1]].remove(gap_left)
    # if following gap abuts new gap
    if gap_right and block_idx + block_span == gap_right[0]:
      new_span += gap_right[1]
      gaps_dict[gap_right[1]].remove(gap_right)
    gaps_dict[new_span].add((new_idx, new_span))
  return checksum3(blocks)

def two(INPUT):
  return two_slow(INPUT)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "9")
  print(p.run(one_fast, 0))
  print(p.run(two_fast, 0))
  print(p.run(two_faster, 0))
  print(p.run(two, 0))

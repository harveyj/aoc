#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  commands = [(command_chunk.split('\n')[0], command_chunk.strip().split('\n')[1:]) for command_chunk in INPUT.split("$ ")][1:]
  return commands

def get_all_sizes(INPUT):
  commands = parse(INPUT)
  def get_dir(root, path):
    wd = root
    for item in path:
      wd = wd[item]
    return wd

  def path_str(path):
    return '/'.join(path)

  def sum_recurse(root, path, all):
    total = 0
    for k in root:
      if type(root[k]) == dict:
        total += sum_recurse(root[k], path + [k], all)
      else:
        print(path, k, root[k])
        total += root[k]
    print(path, total)
    all[path_str(path)] = total
    return total

  root = {}
  path = []

  for command, out in commands:
    bin = command.split()[0]
    if bin == "cd":
      arg = command.split()[1]
      if arg == '..':
        path.pop()
      elif arg == '/':
        path = []
      else:
        path.append(arg)
    elif bin == "ls":
      wd = get_dir(root, path)
      files = out
      for f in files:
        size, name = f.split()
        if size == 'dir':
          wd[name] = {}
        else:
          wd[name] = int(size)
  all_sizes = {}
  root_size = sum_recurse(root, [''], all_sizes)
  all_sizes[path_str(root)] = root_size
  return all_sizes

def one(INPUT):
  all_sizes = get_all_sizes(INPUT)
  total = 0
  for path, val in all_sizes.items():
    if val < 100000:
      total += val
  return total

def two(INPUT):
  CAPACITY = 70000000
  all_sizes = get_all_sizes(INPUT)
  NEEDED = 30000000 - (CAPACITY - all_sizes.get(''))
  print('CAPACITY', 70000000)
  print('USED', all_sizes.get(''))
  print('NEEDED', NEEDED)
  smallest_path = None
  smallest_total = 1000000000000000
  for path, val in all_sizes.items():
    if val >= NEEDED and val < smallest_total:
      print('replacing', smallest_path, path)
      smallest_path = path
      smallest_total = val
  return smallest_path


if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "7")

  p.run(one, 0) 
  p.run(two, 0) 

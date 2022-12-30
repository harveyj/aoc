#!/usr/bin/env python3
import puzzle
import re
from collections import deque, namedtuple

def parse(INPUT):
  ret = []
  for l in INPUT.split('\n'):
    print(l)
    mat = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l)
    ret.append(Spec(*map(int, mat.group(1, 2, 3, 4, 5, 6, 7))))
  return ret

State = namedtuple("State", "ore clay obsidian geodes ore_r clay_r obsidian_r geode_r")
Spec = namedtuple("Spec", "id orc_o crc_o obrc_o obrc_c grc_o grc_ob")

def advance(state, spec, moves):
  (ore_i, clay_i, obsidian_i, geode_i) = moves
  ore = state.ore + state.ore_r - ore_i * spec.orc_o  - clay_i * spec.crc_o - obsidian_i * spec.obrc_o - geode_i * spec.grc_o
  clay = state.clay + state.clay_r - spec.obrc_c * obsidian_i
  obsidian = state.obsidian + state.obsidian_r - spec.grc_ob * geode_i
  geodes = state.geodes + state.geode_r
  ore_r = state.ore_r + ore_i
  clay_r = state.clay_r + clay_i
  obsidian_r = state.obsidian_r + obsidian_i
  geode_r = state.geode_r + geode_i
  return State(ore, clay, obsidian, geodes, ore_r, clay_r, obsidian_r, geode_r)

move_codes = {'o': (1, 0, 0, 0), 'c': (0, 1, 0, 0), 'ob': (0, 0, 1, 0), 'g': (0,0,0,1), 'z': (0,0,0,0)}

def legal(moves, state, spec):
  (or_i, cr_i, obr_i, g_i) = moves
  ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o
  clay = state.clay - obr_i * spec.obrc_c
  obs = state.obsidian - g_i * spec.grc_ob 
  return ore >= 0 and clay >= 0 and obs >= 0

def apply_move(choice, path, elapsed, state, spec, max_ore_robots, max_clay_robots, max_obsidian_robots, END):

  additional_path = ()
  moves = move_codes[choice]

  if choice == 'o' and state.ore_r >= max_ore_robots or choice == 'c' and state.clay_r >= max_clay_robots or choice == 'ob' and state.obsidian_r >= max_obsidian_robots:
    while elapsed != END:
      state = advance(state, spec, move_codes['z'])
      # additional_path += ((choice, elapsed, state),)
      elapsed += 1
    return (path+additional_path, elapsed, state)
  if choice == 'ob' and state.clay_r == 0 or choice == 'g' and state.obsidian_r == 0 or choice == 'g' and state.clay_r == 0:
    return ([], END, state)

  while not legal(moves, state, spec) and elapsed != END:
    state = advance(state, spec, move_codes['z'])
    # additional_path += ((choice, elapsed, state),)
    elapsed += 1

  # if we terminate because the move is now legal, apply the move
  if legal(moves, state, spec) and elapsed < END:
    state = advance(state, spec, moves)
    # additional_path += ((choice, elapsed, state),)
    elapsed += 1
  return (path+additional_path, elapsed, state)

def run_all_sequences(spec, END):
  max_score = 0; max_moves = []

  max_ore_robots = max(spec.orc_o, spec.crc_o, spec.grc_o)
  max_clay_robots = spec.obrc_c
  max_obsidian_robots = spec.grc_ob

  start_state = ((), 0, State(0,0,0,0,1,0,0,0))
  stack = deque([start_state])

  while stack:
    # elapsed is defined as the "you now have x geodes" time from the problem spec
    path, elapsed, state = stack.pop()
    if elapsed == END: 
      if state.geodes > max_score:
        print('new max', state.geodes)
        max_score = state.geodes
        max_moves = path
      continue
    # if elapsed > END: print('ERROR END EXCEEDED')
    time_left = END - elapsed
    geodes_possible = state.geodes + state.geode_r * time_left + time_left * (time_left -1) / 2
    if geodes_possible <= max_score: continue
    for choice in ['o', 'c', 'ob', 'g']:
      stack.append(apply_move(choice, path, elapsed, state, spec, max_ore_robots, max_clay_robots, max_obsidian_robots, END))

  return max_score, max_moves

def one(INPUT):
  specs = parse(INPUT)
  answer = 0
  for spec_id, spec in enumerate(specs):
    max_score, max_moves = run_all_sequences(spec, 24)
    answer += (spec_id + 1) * max_score
  return answer

def two(INPUT):
  specs = parse(INPUT)
  answer = 1
  for spec_id, spec in enumerate(specs[:3]):
    max_score, max_moves = run_all_sequences(spec, 32)
    answer *= max_score
  return answer

p = puzzle.Puzzle("19")
p.run(one, 0)
p.run(two, 0)
#!/usr/bin/env python3
import puzzle
import re
from collections import namedtuple
import itertools

def parse(INPUT):
  ret = []
  for l in INPUT.split('\n'):
    print(l)
    mat = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l)
    ret.append(Spec(*map(int, mat.group(1, 2, 3, 4, 5, 6, 7))))
  return ret

State = namedtuple("State", "ore clay obsidian geodes ore_r clay_r obsidian_r geode_r")
Spec = namedtuple("Spec", "id orc_o crc_o obrc_o obrc_c grc_o grc_ob")

def legal(moves, state, spec):
  (or_i, cr_i, obr_i, g_i) = moves
  ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o
  clay = state.clay - obr_i * spec.obrc_c
  obs = state.obsidian - g_i * spec.grc_ob 
  return ore >= 0 and clay >= 0 and obs >= 0

def advance(state, spec, moves):
  (ore_i, clay_i, obsidian_i, geode_i) = moves
  ore = state.ore + state.ore_r - spec.orc_o * ore_i - spec.crc_o * clay_i - obsidian_i * spec.obrc_o - geode_i*spec.grc_o
  clay = state.clay + state.clay_r - spec.obrc_c * obsidian_i
  obsidian = state.obsidian + state.obsidian_r - spec.grc_ob * geode_i
  geodes = state.geodes + state.geode_r
  ore_r = state.ore_r + ore_i
  clay_r = state.clay_r + clay_i
  obsidian_r = state.obsidian_r + obsidian_i
  geode_r = state.geode_r + geode_i
  return State(ore, clay, obsidian, geodes, ore_r, clay_r, obsidian_r, geode_r)

def one(INPUT):
  ITERS = 24
  specs = parse(INPUT)
  answer = 0
  for spec_id, spec in enumerate(specs[:1]):
    print(spec_id, spec)
    # "ore clay obsidian geodes ore_r clay_r obsidian_r geode_r"
    max_ore = max(spec.orc_o, spec.crc_o, spec.obrc_o, spec.grc_o)
    max_clay = spec.obrc_c
    max_obs = spec.grc_ob
    states = {}
    for raw_state in itertools.product(range(max_ore), range(max_clay), range(max_obs), range(20), range(5), range(5), range(5), range(5)):
      state = State(*raw_state)
      states[(state, 0)] = state.geodes
      # print(state)

  return answer

def two(INPUT):
  return 0

p = puzzle.Puzzle("19")
p.run(one, 1)
p.run(two, 0)

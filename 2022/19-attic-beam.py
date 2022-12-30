#!/usr/bin/env python3
from time import time
import puzzle
import re
import math
from collections import namedtuple, deque
import functools
import networkx as nx

def parse(INPUT):
  ret = []
  for l in INPUT.split('\n'):
    print(l)
    mat = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l)
    ret.append(Spec(*map(int, mat.group(1, 2, 3, 4, 5, 6, 7))))
  return ret

State = namedtuple("State", "ore clay obsidian geodes ore_r clay_r obsidian_r geode_r")
Spec = namedtuple("Spec", "id orc_o crc_o obrc_o obrc_c grc_o grc_ob")

def score(state, spec, time_left, debug=False):
  ore_val = spec.grc_o * spec.orc_o + spec.grc_ob * spec.obrc_o + spec.grc_ob*spec.obrc_c*spec.crc_o
  clay_val = spec.grc_ob * spec.obrc_c
  obsidian_val = spec.grc_ob 
  # ore_val, clay_val, obsidian_val = (100,100,100)

  component_contribution = (math.sqrt(state.ore / ore_val * time_left) 
          * math.sqrt(state.clay / clay_val * time_left)
          * math.sqrt(state.obsidian / obsidian_val* time_left)
          * math.sqrt(state.ore_r * ore_val * time_left) 
          * math.sqrt(state.clay_r * clay_val * time_left) 
          * math.sqrt(state.obsidian_r * obsidian_val *time_left)) / (ore_val * clay_val * obsidian_val * time_left)
  if debug and state.geodes > 0:
    print('ore_val %i, clay_val %i, obsidian_val %i' %(ore_val, clay_val, obsidian_val))
    print("geode contribution %i %i" % (state.geodes, state.geode_r*time_left))
    print("cc", component_contribution)

  return state.geodes + state.geode_r * time_left + component_contribution

def next_states(state, spec):
  def legal(or_i, cr_i, obr_i, g_i, state, spec, time_left=0):
    ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o
    clay = state.clay - obr_i * spec.obrc_c
    obs = state.obsidian - g_i * spec.grc_ob
    max_ore_robots = max(spec.orc_o, spec.crc_o, spec.grc_o)
    max_clay_robots = spec.obrc_c
    max_obsidian_robots = spec.grc_ob
    # Prune these
    if state.ore_r + or_i > max_ore_robots or state.clay_r + cr_i > max_clay_robots or state.obsidian_r + obr_i > max_obsidian_robots:
      # print('prune')
      return False
    return ore >= 0 and clay >= 0 and obs >= 0
  ret = []
  for (or_i, cr_i, obr_i, g_i) in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (0,0,0,0)):
    # print('eval')
    if legal(or_i, cr_i, obr_i, g_i, state, spec):
      new_ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o + state.ore_r
      ret.append(State(ore=new_ore, clay = state.clay - obr_i * spec.obrc_c + state.clay_r, obsidian=state.obsidian - g_i * spec.grc_ob + state.obsidian_r, geodes = state.geodes + state.geode_r,
      ore_r=state.ore_r + or_i, clay_r=state.clay_r+cr_i, obsidian_r=state.obsidian_r+obr_i, geode_r=state.geode_r + g_i))
  return ret

def beam_search(spec, iters, start_state, next_states, score, width):
  states = deque([start_state])
  seen = set()
  for i in range(iters):
    new_states = []
    time_left = iters - i
    for state in states:
      if state in seen: continue
      seen.add(state)
      new_states.extend(next_states(state, spec))
    print(i, len(states))
    new_states = sorted(new_states, key=functools.partial(score, spec=spec, time_left=time_left))
    new_states = new_states[-width:]
    states = new_states
  return states

def one(INPUT):
  ITERS = 24
  specs = parse(INPUT)
  start_state = State(ore=0, clay=0, obsidian=0, geodes=0, ore_r=1, clay_r=0, obsidian_r=0, geode_r=0)
  answer = 0
  for i, spec in enumerate(specs):
    states = beam_search(spec, ITERS, start_state, next_states, score, width=50000)
    for s in states[-1:]:
      print(s.geodes)
      answer += (i+1) * s.geodes
  return answer

def two(INPUT):
  return 0

p = puzzle.Puzzle("19")
p.run(one, 0)
p.run(two, 0)

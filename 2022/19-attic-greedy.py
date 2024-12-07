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
  for l in INPUT:
    print(l)
    mat = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l)
    ret.append(Spec(*map(int, mat.group(1, 2, 3, 4, 5, 6, 7))))
  return ret

State = namedtuple("State", "ore clay obsidian geodes ore_r clay_r obsidian_r geode_r")
Spec = namedtuple("Spec", "id orc_o crc_o obrc_o obrc_c grc_o grc_ob")

# def score(state, spec, time_left, debug=False):
#   ore_val = spec.grc_o * spec.orc_o + spec.grc_ob * spec.obrc_o + spec.grc_ob*spec.obrc_c*spec.crc_o
#   clay_val = spec.grc_ob * spec.obrc_c
#   obsidian_val = spec.grc_ob 
#   # ore_val, clay_val, obsidian_val = (100,100,100)

#   component_contribution = (math.sqrt(state.ore / ore_val) 
#           * math.sqrt(state.clay / clay_val)
#           * math.sqrt(state.obsidian / obsidian_val)
#           * math.sqrt(state.ore_r * ore_val * time_left) 
#           * math.sqrt(state.clay_r * clay_val * time_left) 
#           * math.sqrt(state.obsidian_r * obsidian_val *time_left)) / (ore_val * clay_val * obsidian_val * time_left)
#   if debug and state.geodes > 0:
#     print('ore_val %i, clay_val %i, obsidian_val %i' %(ore_val, clay_val, obsidian_val))
#     print("geode contribution %i %i" % (state.geodes, state.geode_r*time_left))
#     print("cc", component_contribution)

#   return state.geodes + state.geode_r * time_left + component_contribution

def next_states(state, spec):
  def legal(or_i, cr_i, obr_i, g_i, state, spec):
    ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o
    clay = state.clay - obr_i * spec.obrc_c
    obs = state.obsidian - g_i * spec.grc_ob 
    return ore >= 0 and clay >= 0 and obs >= 0
  ret = []
  for or_i in range(state.ore // spec.orc_o + 1):
    for cr_i in range(state.ore // spec.crc_o + 1):
      for obr_i in range(min(state.ore // spec.obrc_o, state.clay // spec.obrc_c) + 1):
        for g_i in range(min(state.ore // spec.grc_o, state.obsidian // spec.grc_ob) + 1):
          if legal(or_i, cr_i, obr_i, g_i, state, spec):
            # If you can buy *anything* buying *something* is the dominant option
            if legal(or_i+1, cr_i+1, obr_i+1, g_i+1, state, spec):
              print('can buy more of anything')
              continue
            new_ore = state.ore - or_i * spec.orc_o - cr_i * spec.crc_o - obr_i * spec.obrc_o - g_i * spec.grc_o + state.ore_r
            ret.append(State(ore=new_ore, clay = state.clay - obr_i * spec.obrc_c + state.clay_r, obsidian=state.obsidian - g_i * spec.grc_ob + state.obsidian_r, geodes = state.geodes + state.geode_r,
            ore_r=state.ore_r + or_i, clay_r=state.clay_r+cr_i, obsidian_r=state.obsidian_r+obr_i, geode_r=state.geode_r + g_i))
  return ret

# def beam_search(spec, iters, start_state, next_states, score, width):
#   states = deque([start_state])
#   seen = set()
#   for i in range(iters):
#     new_states = []
#     time_left = iters - i
#     for state in states:
#       if state in seen: continue
#       seen.add(state)
#       new_states.extend(next_states(state, spec))
#     new_states = sorted(new_states, key=functools.partial(score, spec=spec, time_left=time_left))
#     new_states = new_states[-width:]
#     for ns in new_states[-5:]:
#       print(ns, score(ns, spec, time_left, debug=True))
#     states = new_states
#   return states

def create_graph(spec, iters, start_state, next_states):
  # def dominated(state, states):
  #   for other in states:
  #     if state.ore <= other.ore and state.clay <= other.clay and state.geodes <= other.geodes and state.obsidian <= other.obsidian and state.ore_r <= other.ore_r and state.clay_r <= other.clay_r and state.obsidian_r <= other.obsidian_r and state.geode_r <= other.geode_r:
  #       return True
  #   return False
  G = nx.DiGraph()
  states = deque([start_state])
  seen = set()
  for i in range(iters):
    new_states = []
    time_left = iters - i
    for state in states:
      if state in seen: continue
      seen.add(state)
      G.add_node(state)
      for ns in next_states(state, spec):
        G.add_node(ns)
        G.add_edge(state, ns)
        new_states.append(ns)
    print(i, G)
    states = new_states
  return G

def one(INPUT):
  ITERS = 24
  specs = parse(INPUT)
  start_state = State(ore=0, clay=0, obsidian=0, geodes=0, ore_r=1, clay_r=0, obsidian_r=0, geode_r=0)
  for s in specs[:1]:
    G = create_graph(s, ITERS, start_state, next_states)
  return 0

def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "19")

  p.run(one, 0) 
  p.run(two, 0) 

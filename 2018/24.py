#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict, namedtuple

Unit = namedtuple('Unit', ['id', 'n', 'team', 'hp', 'attack', "attacktype", 'initiative', 'weaknesses', 'immunities'])

def extract_unit(raw_unit, team, i):
  n, hp, attack, initiative = library.ints(raw_unit)
  words = raw_unit.split()
  damage_idx = words.index('damage')
  attacktype = words[damage_idx-1]
  immunities = tuple()
  immune_match = re.search(r'immune to ([\w ,]+)', raw_unit)
  if immune_match:
    print(immune_match.groups())
    immunities = tuple(immune_match.groups()[0].split(', '))
  weaknesses = tuple()
  weak_match = re.search(r'weak to ([\w ,]+)', raw_unit)
  if weak_match:
    weaknesses = tuple(weak_match.groups()[0].split(', '))
  return Unit(team+str(i+1), n, team, hp, attack, attacktype, initiative, weaknesses, immunities)

def parse_input(INPUT):
  immune_raw, infection_raw = '\n'.join(INPUT).split('\n\n')
  immune = immune_raw.split('\n')[1:]
  infection = infection_raw.split('\n')[1:]
  units = []
  for i, raw_unit in enumerate(immune):
    units.append(extract_unit(raw_unit, 'immune', i))
  for i, raw_unit in enumerate(infection):
    units.append(extract_unit(raw_unit, 'infection', i))
  return units

def ep(unit):
  return unit.attack * unit.n

def dmg(a, b):
  base = ep(a)
  if a.attacktype in b.immunities: return 0
  if a.attacktype in b.weaknesses: return base * 2
  return base

def one(INPUT):
  units = parse_input(INPUT)
  all_units = {u.id:u for u in units}
  for u in all_units.values(): print(u)
  while True:
    if len(set([u.team for u in all_units.values()])) == 1:
      return sum([u.n for u in all_units.values()])
    # Targeting phase
    tgts = dict()
    unit_order = sorted(all_units.values(), key=lambda a: (-ep(a), -a.initiative))
    for unit in unit_order:
      untargeted = [u for u in all_units.values() if u.id not in tgts.values() and u.team != unit.team]
      all_tgts = sorted(untargeted, key=lambda a: (-dmg(unit, a), -ep(a), -a.initiative))
      # for t in all_tgts:
      #   print(f'{unit.id} would deal {t.id} {dmg(unit, t)}')
      if not all_tgts: continue
      tgt = all_tgts[0]
      if dmg(unit, tgt) > 0:
        tgts[unit.id] = tgt.id
    # Attack phase
    unit_order = sorted(all_units.values(), key=lambda a: -a.initiative)
    for attacker in unit_order:
      if attacker.id not in tgts or attacker.id not in all_units: continue
      attacker = all_units[attacker.id]
      tgt = [all_units[id] for id in all_units if all_units[id].id == tgts[attacker.id]][0]
      killed = dmg(attacker, tgt) // tgt.hp
      if killed >= tgt.n:
        del all_units[tgt.id]
        killed = tgt.n
      else:
        post_attack = Unit(id=tgt.id, n=tgt.n-killed, team=tgt.team, hp = tgt.hp, attack=tgt.attack, attacktype=tgt.attacktype,
                            initiative=tgt.initiative, weaknesses=tgt.weaknesses, immunities=tgt.immunities)
        all_units[tgt.id] = post_attack
      # print(f'{attacker.id} attacks defending group {tgt.id} killing {killed}')
    for key in all_units:
      print(all_units[key])

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out


if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "24")
  print(p.run(one, 0))
  # print(p.run(two, 0))
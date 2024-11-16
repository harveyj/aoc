#!/usr/bin/env python3
import puzzle
import itertools

def turn(params, t, debug = False, hard=False):
  h_hp, h_m, h_sh, h_rc, b_hp, b_a, b_p, consumed = params
  if hard:
    h_hp -= 1
  if h_hp <= 0:
    # print('ERROR: you die')
    return None

  debug and print('-- Player turn --')
  debug and print(f'- Player has {h_hp} hit points, {7 if h_sh > 0 else 0} armor, {h_m} mana')
  debug and print(f'- Boss has {b_hp} hit points')
  debug and print(f'- Player casts {t}.')
  if b_p > 0: 
    b_p = max(b_p-1, 0)
    debug and print(f'Poison deals 3 damage; its timer is now {b_p}.')
    b_hp -= 3
  if h_rc: 
    h_rc = max(h_rc-1, 0)
    debug and print(f'Recharge provides 101 mana; its timer is now {h_rc}.')
    h_m += 101

  if t == "mm":
    b_hp -= 4
    h_m -= 53
    consumed += 53
  elif t == "dr":
    h_hp += 2
    b_hp -= 2
    h_m -= 73
    consumed += 73
  elif t == "sh":
    if h_sh > 0:
      # print('ERROR re-shield')
      return None
    h_sh = 7
    h_m -= 113
    consumed += 113
  elif t == "p":
    if b_p > 0: 
      # print('ERROR re-poison')
      return None
    b_p = 6
    h_m -= 173
    consumed += 173
  elif t == "re":
    if h_rc > 0: 
      # print('ERROR re-recharge')
      return None
    h_rc = 5
    h_m -= 229
    consumed += 229
  if h_m < 0: 
    # print('ERROR: negative mana')
    return None
  if b_hp <= 0:
    debug and print('boss died')
    return (h_hp, h_m, h_sh, h_rc, b_hp, b_a, b_p, consumed)
  h_sh = max(h_sh-1, 0);  

  debug and print('-- Boss turn --')
  debug and print(f'- Player has {h_hp} hit points, {7 if h_sh > 0 else 0} armor, {h_m} mana')
  debug and print(f'- Boss has {b_hp} hit points')

  if b_p > 0: 
    b_hp -= 3
    debug and print(f'Poison deals 3 damage; its timer is now {b_p}.')
  if h_rc: 
    h_rc = max(h_rc-1, 0)
    debug and print(f'Recharge provides 101 mana; its timer is now {h_rc}.')
    h_m += 101
  if b_hp <= 0:
    debug and print('boss died')
    return (h_hp, h_m, h_sh, h_rc, b_hp, b_a, b_p, consumed)

  debug and print(f'- Boss attacks for {b_a-7 if h_sh > 0 else b_a} damage')
  h_hp -= max(b_a - (7 if h_sh else 0), 1)
  if h_hp <= 0:
    # print('ERROR: you die')
    return None
  h_sh = max(h_sh-1, 0); b_p = max(b_p-1, 0); 

  return (h_hp, h_m, h_sh, h_rc, b_hp, b_a, b_p, consumed)

def one(INPUT):
  legal_turns = ['p', 're', 'sh', 'mm', 'dr']
  sequences = itertools.product(legal_turns, repeat=9)
  total = 0
  consumed = [10000000]
  for sequence in sequences:
    total += 1
    params = 50, 500, 0, 0, 55, 8, 0, 0
    for t in sequence:
      params = turn(params, t)
      if params == None:
        break
    if params:
      if params[4] <= 0:
        consumed.append(params[7])
  return min(consumed)

def two(INPUT):
  legal_turns = ['p', 're', 'sh', 'mm', 'dr']
  sequences = itertools.product(legal_turns, repeat=9)
  total = 0
  consumed = [10000000]
  for sequence in sequences:
    total += 1
    params =  50, 500, 0, 0, 55, 8, 0, 0
    for t in sequence:
      params = turn(params, t, hard=True)
      if params == None:
        break
    if params:
      if params[4] <= 0:
        consumed.append(params[7])
  return min(consumed)

p = puzzle.Puzzle("2015", "22")
p.run(one, 0)
p.run(two, 0)

#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')
  for l in INPUT:
    yield re.match(pat, l).groups()


def one(INPUT):
  ingredients = list(parse(INPUT))
  ing_map = dict()
  for i in ingredients:
    ing_map[i[0]] = tuple(map(int, i[1:5]))
  cap = [ing_map[key][0] for key in ing_map]
  dur = [ing_map[key][1] for key in ing_map]
  fla = [ing_map[key][2] for key in ing_map]
  tex = [ing_map[key][3] for key in ing_map]
  score_max = 0
  for a in range(0, 100):
    for b in range(0, 100-a):
     for c in range(0, 100-a-b):
        d = 100 - a - b -c
        # b = 100 - a
        c_s = a * cap[0] + b * cap[1] + c * cap[2] + d * cap[3]
        d_s = a * dur[0] + b * dur[1] + c * dur[2] + d * dur[3]
        f_s = a * fla[0] + b * fla[1] + c * fla[2] + d * fla[3]
        t_s = a * tex[0] + b * tex[1] + c * tex[2] + d * tex[3]
        if c_s < 0 or d_s < 0 or f_s < 0 or t_s < 0:
          continue
        score = c_s * d_s * f_s * t_s
        if score > score_max:
          score_max = score
  return score_max

def two(INPUT):
  ingredients = list(parse(INPUT))
  ing_map = dict()
  for i in ingredients:
    ing_map[i[0]] = tuple(map(int, i[1:6]))
  cap = [ing_map[key][0] for key in ing_map]
  dur = [ing_map[key][1] for key in ing_map]
  fla = [ing_map[key][2] for key in ing_map]
  tex = [ing_map[key][3] for key in ing_map]
  cal = [ing_map[key][4] for key in ing_map]
  score_max = 0
  for a in range(0, 100):
    for b in range(0, 100-a):
     for c in range(0, 100-a-b):
        d = 100 - a - b -c
        # b = 100 - a
        c_s = a * cap[0] + b * cap[1] + c * cap[2] + d * cap[3]
        d_s = a * dur[0] + b * dur[1] + c * dur[2] + d * dur[3]
        f_s = a * fla[0] + b * fla[1] + c * fla[2] + d * fla[3]
        t_s = a * tex[0] + b * tex[1] + c * tex[2] + d * tex[3]
        cal_s = a * cal[0] + b * cal[1] + c * cal[2] + d * cal[3]
        if c_s < 0 or d_s < 0 or f_s < 0 or t_s < 0:
          continue
        score = c_s * d_s * f_s * t_s
        if score > score_max and cal_s == 500:
          score_max = score
  return score_max
p = puzzle.Puzzle("2015", "15")
p.run(one, 0)
p.run(two, 0)

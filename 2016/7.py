#!/usr/bin/env python3
import puzzle
import re

def one(INPUT):
  pattern = re.compile(r'(\w)(\w)\2\1')
  pattern_brackets = re.compile(r'\[.*?\]')
  legal = set()
  for l in INPUT:
    found = False; illegal = False
    for match in re.finditer(pattern, l):
      if match.group()[0] == match.group()[1]: continue
      found = True
      illegal_zones = re.finditer(pattern_brackets, l)
      for iz in illegal_zones:
        if iz.span()[0] < match.span()[0] < iz.span()[1]:
          illegal = True
    if found and not illegal:
      legal.add(l)
  return len(legal)

def palindrome(str):
  for i in range(len(str)-2):
    if str[i] in '[]' or str[i+1] in '[]': continue
    if str[i] == str[i+2]:
      yield {'chars': (str[i], str[i+1]), 'pos': (i, i+2)}

def two(INPUT):
  pattern_brackets = re.compile(r'\[.*?\]')
  legal = set()
  illegal = set()
  matches = set()
  for l in INPUT:
    for match in palindrome(l):
      a, b = match['chars']
      s, e = match['pos']
      if a == b: 
        continue
      inner_zones = re.finditer(pattern_brackets, l)
      inner = False
      for iz in inner_zones:
        if iz.span()[0] < s < iz.span()[1]:
          inner = True
          break
      if inner == False:
        inner_zones = re.finditer(pattern_brackets, l)
        for iz in inner_zones:
          for inner_match in palindrome(iz.group()):
            c, d = inner_match['chars']
            if a == d and b == c: 
              legal.add(l)
      if l not in legal:
        illegal.add(l)
  for m in matches: print(m)
  return len(legal)

p = puzzle.Puzzle("2016", "7")
p.run(one, 0)
p.run(two, 0)

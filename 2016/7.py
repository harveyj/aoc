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
      print('ms', match.span())
      illegal_zones = re.finditer(pattern_brackets, l)
      for iz in illegal_zones:
        print('iz', iz.span())
        if iz.span()[0] < match.span()[0] < iz.span()[1]:
          print('illegal')
          illegal = True
    if found and not illegal:
      legal.add(l)
  print(legal)

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
    # pals = list(palindrome(l))
    # char_pairs = [pal['chars'] for pal in pals]
    # for cp in char_pairs:
    #   if (cp[1], cp[0]) in char_pairs and cp[0] != cp[1]:
    #     print('MATCH', cp)
    #     matches.add(l)
    # continue
    # print(char_pairs)
    for match in palindrome(l):
      a, b = match['chars']
      s, e = match['pos']
      if a == b: 
        print('bail dup', a, b)
        continue
      inner_zones = re.finditer(pattern_brackets, l)
      print(f'om {a}, {b}')
      inner = False
      for iz in inner_zones:
        print('iz', iz.group(), iz.span())
        if iz.span()[0] < s < iz.span()[1]:
          print('bail within iz')
          inner = True
          break
      if inner == False:
        inner_zones = re.finditer(pattern_brackets, l)
        for iz in inner_zones:
          for inner_match in palindrome(iz.group()):
            # print('im', inner_match)
            c, d = inner_match['chars']
            # print(f'c: {c}, d: {d}')
            if a == d and b == c: 
              print('FOUND', a, b)
              legal.add(l)
      if l not in legal:
        illegal.add(l)
  # print('illegal', illegal)
  for m in matches: print(m)
  return len(legal)

p = puzzle.Puzzle("7")
# p.run(one, 0)
p.run(two, 0)

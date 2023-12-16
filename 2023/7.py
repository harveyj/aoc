#!/usr/bin/env python3
import puzzle
from collections import Counter
from collections import namedtuple
from operator import itemgetter, attrgetter

def parse_input(INPUT):
  return [(list(l.split()[0]), int(l.split()[1])) for l in INPUT.split('\n')]


def one(INPUT):
  (HIGH, ONE, TWO, THREE, FULL, FOUR, FIVE) = range(7)
  CARDS = dict(zip(list('23456789TJQKA'), range(2,15)))
  Hand = namedtuple('Hand', ['code', "a", "b", "c", "d", "e", ])
  invals = parse_input(INPUT)
  hands = []
  scores = dict()
  for cards, score in invals:
    code = -1
    c = Counter(cards)
    mc = c.most_common()[0]
    mc2 = c.most_common()[1] if len(c.most_common()) > 1  else [c,0]
    second_pair = mc2[1] == 2
    if mc[1] == 5: code = FIVE
    elif mc[1] == 4: code = FOUR
    elif mc[1] == 3: code = FULL if second_pair else THREE
    elif mc[1] == 2: code = TWO if second_pair else ONE
    elif mc[1] == 1: code = HIGH
    h = Hand(code, *[CARDS[c] for c in cards])
    hands.append(h)
    scores[h] = score
  sorted_hands = sorted(hands, key=attrgetter('code', 'a', 'b', 'c', 'd', 'e', ))
  out = 0
  for i, h in enumerate(sorted_hands):
    out += (i + 1) * scores[h]
  for sh in sorted_hands: print(sh)
  return out

def two(INPUT):
  (HIGH, ONE, TWO, THREE, FULL, FOUR, FIVE) = range(7)
  JOKER_HIGH_MAP = {HIGH: ONE, ONE: THREE, TWO: FOUR, THREE: FIVE, FULL: FIVE, FOUR: FIVE, FIVE: FIVE }
  JOKER_LOW_MAP = {HIGH: ONE, ONE: THREE, TWO: FULL, THREE: FOUR, FULL: FIVE, FOUR: FIVE, FIVE: FIVE }
  CARDS = dict(zip(list('J23456789TQKA'), range(2,15)))
  Hand = namedtuple('Hand', ['code', "a", "b", "c", "d", "e"])
  invals = parse_input(INPUT)
  hands = []
  scores = dict()
  for cards, score in invals:
    code = -1
    c = Counter(cards)
    mc = c.most_common()[0]
    mc2 = c.most_common()[1] if len(c.most_common()) > 1  else [c,0]
    second_pair = mc2[1] == 2
    if mc[1] == 5: code = FIVE
    elif mc[1] == 4: code = FOUR
    elif mc[1] == 3: code = FULL if second_pair else THREE
    elif mc[1] == 2: code = TWO if second_pair else ONE
    elif mc[1] == 1: code = HIGH
    
    if code == TWO and mc2[0] == 'J':
      code = FOUR
    elif mc[0] == 'J':
      code = JOKER_HIGH_MAP[code]
    elif 'J' in cards:
      code = JOKER_LOW_MAP[code]
    h = Hand(code, *[CARDS[c] for c in cards])
    hands.append(h)
    scores[h] = score
  sorted_hands = sorted(hands, key=attrgetter('code', 'a', 'b', 'c', 'd', 'e', ))
  out = 0
  for i, h in enumerate(sorted_hands):
    out += (i + 1) * scores[h]
  for sh in sorted_hands: print(sh)
  return out

p = puzzle.Puzzle("7")
# p.run(one, 0)
p.run(two, 0)

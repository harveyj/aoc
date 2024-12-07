import puzzle
import collections
import itertools

Row = collections.namedtuple('Row', ['tests', 'values'])

def process_input(INPUT):
  rows = []
  for line in INPUT:
    l, r = line.split("|");
    tests = l.strip().split(" ");
    values = r.strip().split(" ");
    rows.append(Row(tests=tests, values=values))
  return rows

def one(INPUT):
  processed_input = process_input(INPUT)
  return sum(([sum([1 if len(v) in [2,3,4,7] else 0 for v in row.values]) for row in processed_input]))

def two(INPUT):
  known = { "aa": "", "bb": "", "cc": "", "dd": "", "ee": "", "ff": "", "gg": "" }
  knownNumbers = ["", "", "", "", "", "", "", "", "", ""]
  ccff = ""
  values = []
  processed_input = process_input(INPUT)
  for row in processed_input:
    for test in row.tests:
      if len(test) == 2:
        ccff = test
        knownNumbers[1] = test
      elif len(test) == 4:
        knownNumbers[4] = test
      elif len(test) == 3:
        knownNumbers[7] = test
      elif len(test) == 7:
        knownNumbers[8] = test

    for test in row.tests:
      if len(test) == 6:
        for c in ccff:
          if not c in test:
            known['cc'] = c
            known['ff'] = ccff.replace(c, "")
            knownNumbers[6] = test

    for test in row.tests:
      if len(test) == 5:
        if not known['ff'] in test:
          knownNumbers[2] = test
        elif not known["cc"] in test:
          knownNumbers[5] = test
        else:
          knownNumbers[3] = test

    for test in row.tests:
      if len(test) == 6 and test != knownNumbers[6]:
        allFound = True;
        for c in knownNumbers[3]:
          if not c in test:
            allFound = False
        if allFound:
          knownNumbers[9] = test
        else:
          knownNumbers[0] = test
    for i in range(len(knownNumbers)):
      sv = list(knownNumbers[i])
      sv.sort()
      knownNumbers[i] = ''.join(sv)
    num = "";
    for numSegments in row.values:
      seg = ''.join(sorted(list(numSegments)))
      num += str(knownNumbers.index(seg))
    values.append(int(num));
  return sum(values)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "8")

  p.run(one, 0) 
  p.run(two, 0) 

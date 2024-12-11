import puzzle
import collections

Point = collections.namedtuple('Point', ['x', 'y'])
Line = collections.namedtuple('Line', ['start', 'end'])

def process_input(INPUT):
  ret = []
  for line in INPUT:
    vals = line.split(" -> ");
    start = [int(a) for a in vals[0].split(",")]
    end = [int(a) for a in vals[1].split(",")]
    ret.append(Line(
      start=Point(x=start[0], y=start[1]),
      end=Point(x=end[0], y=end[1])))
  return ret

def puzz(INPUT, diag=False):
  processed_input = process_input(INPUT)
  overlaps = collections.defaultdict(int)
  for line in processed_input:
    if line.start.x == line.end.x:
      for y in range(line.start.y, line.end.y+1):
        overlaps[(line.start.x, y)] += 1
      for y in range(line.end.y, line.start.y+1):
        overlaps[(line.start.x, y)] += 1
    elif line.start.y == line.end.y:
      for x in range(line.start.x, line.end.x+1):
        overlaps[(x, line.start.y)] += 1
      for x in range(line.end.x, line.start.x+1):
        overlaps[(x, line.start.y)] += 1
    elif diag:
      delta = abs(line.start.x - line.end.x)
      dx = 1 if line.start.x < line.end.x else -1
      dy = 1 if line.start.y < line.end.y else -1
      for i in range(delta+1):
        overlaps[(line.start.x + i * dx, line.start.y + i * dy)] += 1
  overlapCount = len([overlap for overlap in overlaps.values() if overlap > 1])
  return overlapCount;

def one(INPUT):
  return puzz(INPUT, diag=False)
def two(INPUT):
  return puzz(INPUT, diag=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "5")

  p.run(one, 0) 
  p.run(two, 0) 
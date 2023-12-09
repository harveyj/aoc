import copy

class Puzzle(object):

  def __init__(self, id):
    self.id = id
    self.inputs = open('inputs/' + id + '.txt').read().split('\n\n\n')

  def run(self, fn, input_id, user_input=None, **kwarg):
    if user_input:
      answer = fn(self.inputs[input_id], copy.copy(user_input), **kwarg)
    else:
      answer = fn(self.inputs[input_id], **kwarg)
    print("ANSWER", answer)
    return answer


class Grid:

  def __init__(self, x=0, y=0, grid=None):
    if grid:
      self.grid = grid
    else:
      self.grid = [["." for i in range(self.x)] for j in range(self.y + 1)]
    self.overlays = []

  NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  NEIGHBORS_DIAG = NEIGHBORS + [(-1, -1), (1, -1), (1, 1), (-1, 1)]

  def max_x(self):
    return len(self.grid[0])

  def max_y(self):
    return len(self.grid)

  def set(self, pt, val):
    x, y = pt
    self.grid[y][x] = val

  def get(self, pt, default=None):
    x, y = pt
    if x < 0 or y < 0 or x >= self.max_x() or y >= self.max_y():
      return default
    return self.grid[y][x]

  def neighbors(self, pt):
    x, y = pt
    return filter(
        lambda a: a != None,
        [self.get((x + DX, y + DY)) for DX, DY in self.NEIGHBORS],
    )

  def neighbors_diag(self, pt):
    x, y = pt
    return filter(
        lambda a: a != None,
        [self.get((x + DX, y + DY)) for DX, DY in self.NEIGHBORS_DIAG],
    )

  def neighbors_diag_locs(self, pt):
    x, y = pt
    return [(x + DX, y + DY) for DX, DY in self.NEIGHBORS_DIAG]



  def __str__(self):
    rows = []
    for y, row in enumerate(self.grid):
      row_out = []
      for x, cell in enumerate(row):
        if (x, y) in self.overlays:
          row_out.append(self.overlays[(x, y)])
        else:
          row_out.append(cell)
      rows.append(''.join(row_out))
    return '\n'.join(rows)

  def window(self, min_x, min_y, max_x, max_y):
    return '\n'.join(
        [''.join(row[min_x:max_x]) for row in self.grid[min_y:max_y]])

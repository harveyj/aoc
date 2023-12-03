class Grid:
  def __init__(self, default_val, x, y):
    self.x = x; self.y = y
    self.grid = [[default_val for i in range(x)] for j in range(y)]

  def set(self, pt, val):
    x, y = pt
    self.grid[y][x] = val

  def get(self, pt):
    x, y = pt
    return self.grid[y][x]

  def __str__(self):
    return '\n'.join([''.join(row) for row in self.grid])

  def window(self, min_x, min_y, max_x, max_y):
    return '\n'.join([''.join(row[min_x:max_x]) for row in self.grid[min_y:max_y]])


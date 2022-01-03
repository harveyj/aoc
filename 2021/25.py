import puzzle

# 0 is main
# 1 is test

def run(INPUT):
  def down_coord(x, y, downs, rights):
    new = (x, (y+1)% len(grid))
    if new in downs or new in rights:
      return (x, y)
    return new
  def right_coord(x, y, downs, rights):
    new = ((x+1)% len(grid[0]), y)
    if new in downs or new in rights:
      return (x, y)
    return new
  def print_grid(grid, downs, rights):
    grid = [['.' for x in range(len(grid[0]))] for y in range(len(grid))]
    for (x, y) in downs:
      grid[y][x] = '>'
    for (x, y) in rights:
      grid[y][x] = 'v'
    for row in grid:
      print(''.join(row))
    print('')
  grid = [list(l) for l in INPUT.split('\n')]
  rights = [(x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == '>']
  downs = [(x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'v']
  for i in range(1000):
    # print_grid(grid, downs, rights)
    new_rights = [right_coord(*pt, downs, rights) for pt in rights]
    rights_move = new_rights != rights
    new_downs = [down_coord(*pt, downs, new_rights) for pt in downs]
    downs_move = new_downs != downs
    if not downs_move and not rights_move:
      print(i+1)
      return
    downs = new_downs
    rights = new_rights

p = puzzle.Puzzle("25")
p.run(run, 0)

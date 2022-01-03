import puzzle

def process_input(intext):
  dot_text, fold_text = intext.split("\n\n")
  dots = {(int(a.split(",")[0]), int(a.split(",")[1])): True for a in dot_text.split("\n")}
  folds = []
  for line in fold_text.split("\n"):
    l, r = line.split("=")
    if 'x' in l:
      folds.append((int(r), 1000000))
    else: 
      folds.append((1000000, int(r)))
  return dots, folds

def fold(dots, xsplit, ysplit):
  new_dots = {}
  for x, y in dots:
    if y > ysplit:
      y = ysplit - (y - ysplit)
    if x > xsplit:
      x = xsplit - (x - xsplit)
    new_dots[(x, y)] = True
  return new_dots

def render(dots):
  grid = [[' ' for x in range(50)] for y in range(50)] 
  for x, y in dots:
    grid[x][y] = "X"
  return '\n'.join([''.join(row) for row in grid])

def one(intext):
  dots, folds = process_input(intext)
  dots = fold(dots, *folds[0])
  print("PART ONE ANSWER", len(dots))
  
def two(intext):
  dots, folds = process_input(intext)
  for f in folds:
    dots = fold(dots, *f)
  print("PART TWO ANSWER:\n", render(dots))

p = puzzle.Puzzle("13")
p.run(one, 0)
p.run(two, 0)
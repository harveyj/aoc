#!/usr/bin/env python3
import puzzle, library

def one(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  G2 = library.Grid(x=G.max_x(), y=G.max_y())
  DIRS_ALL = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
  # DIRS_ALL = [(1, 1)]
  seen = []
  for dx, dy in DIRS_ALL:
    for x in range(G.max_x()+1):
      for y in range(G.max_y()+1):
        out = ''
        nx, ny = x, y
        for _ in range(4):
          out += G.get((nx, ny), default="")
          nx += dx; ny += dy
        print(out)
        if out == 'XMAS':
          seen.append(((x, y), dir))
          nx, ny = x, y
          for _ in range(4):
            G2.set((nx, ny), G.get((nx, ny)))
            nx += dx; ny += dy
  # print(G2)
  return len(seen)

def two(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  Gnesw = library.Grid(x=G.max_x(), y=G.max_y())
  Gnwse = library.Grid(x=G.max_x(), y=G.max_y())
  DIRS_NESW = [ (1, -1), (-1, 1)]
  DIRS_NWSE = [(1, 1), (-1, -1),]
  sets = ((Gnesw, DIRS_NESW), (Gnwse, DIRS_NWSE))
  for G2, DIRS in sets:
    for dx, dy in DIRS:
      for x in range(G.max_x()+1):
        for y in range(G.max_y()+1):
          out = ''
          nx, ny = x, y
          for _ in range(3):
            out += G.get((nx, ny), default="")
            nx += dx; ny += dy
          print(out)
          if out == 'MAS':
            nx, ny = x, y
            for _ in range(3):
              G2.set((nx, ny), G.get((nx, ny)))
              nx += dx; ny += dy
  pts = [(x, y) for x in range(G.max_x()) for y in range(G.max_y()) if Gnesw.get((x, y)) == 'A' and Gnwse.get((x, y)) == 'A']
  return len(pts)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "4")

  p.run(one, 0)
  p.run(two, 0)

import puzzle

def process_input(INPUT):
  lines = INPUT.split("\n\n")
  calls = map(int, lines[0].split(','))
  boards = [[list(map(int, row.split())) for row in b.split("\n")] for b in lines[1:]]
  return calls, boards

def getIndices(i, n, max, mode):
  if mode == "row":
    return { 'x': i, 'y': n }
  elif mode == "col":
    return { 'x': n, 'y': i }
  elif mode == "diag1":
    return { 'x': n, 'y': n }
  elif mode == "diag2":
    return { 'x': max - n - 1, 'y': n }

def isWinner(board):
  modes = ["row", "col"];
  for m in modes:
    for i in range(len(board[0])):
      if (m == "diag1" or m == "diag2") and i > 0:
        break
      allX = True;
      for n in range(len(board[0])):
        indices = getIndices(i, n, len(board[0]), m)
        if board[indices['x']][indices['y']] != "X":
          allX = False
      if allX:
        return True

def calcScore(board):
  total = 0;
  for i in range(len(board[0])):
    for j in range(len(board[0])):
      if board[i][j] != "X":
        total += board[i][j]
  return total;

def call(call, board):
  return [["X" if c == call else c for c in row] for row in board]

def one(INPUT):
  calls, boards = process_input(INPUT)
  for c in calls:
    for b_i in range(len(boards)):
      boards[b_i]=call(c, boards[b_i])
      if isWinner(boards[b_i]):
        return calcScore(boards[b_i]) * c;


def two(INPUT):
  calls, boards = process_input(INPUT)
  winners = set()
  for c in calls:
    for b_i in range(len(boards)):
      boards[b_i]=call(c, boards[b_i])
      if isWinner(boards[b_i]):
        # print('\n'.join([str(row) for row in boards[b_i]]))
        winners.add(b_i)
        # print()
      if len(winners) == len(boards):
        return calcScore(boards[b_i]) * c;

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "4")

  p.run(one, 0) 
  p.run(two, 0) 

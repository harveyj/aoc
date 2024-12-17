module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 4!`
)}






function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(){return(
function (input) {
  let chunks = input.split("\n\n");
  let calls = chunks[0].split(",").map((a) => a * 1);
  chunks.shift();
  let boards = [];
  for (let i = 0; i < chunks.length; i++) {
    let board = [];
    let boardRows = chunks[i].split("\n");
    for (let br of boardRows) {
      board.push(
        br
          .trim()
          .split(new RegExp(" +"))
          .map((a) => a * 1)
      );
    }
    boards.push(board);
  }
  return { calls, boards };
}
)}

function _ANSWER_1(input)
{
  let myInput = JSON.parse(JSON.stringify(input));
  function callOut(call) {
    for (let b of myInput.boards) {
      for (let br of b) {
        for (let i = 0; i < br.length; i++) {
          if (br[i] == call) {
            br[i] = "X";
          }
        }
      }
    }
  }
  function getIndices(i, n, max, mode) {
    if (mode == "row") {
      return { x: i, y: n };
    } else if (mode == "col") {
      return { x: n, y: i };
    } else if (mode == "diag1") {
      return { x: n, y: n };
    } else if (mode == "diag2") {
      return { x: max - n - 1, y: n };
    }
  }
  function isWinner(board) {
    let modes = ["row", "col"];
    for (let m of modes) {
      for (let i = 0; i < board[0].length; i++) {
        if ((m == "diag1" || m == "diag2") && i > 0) {
          break;
        }
        let allX = true;
        for (let n = 0; n < board[0].length; n++) {
          let indices = getIndices(i, n, board[0].length, m);
          if (board[indices.x][indices.y] != "X") {
            allX = false;
          }
        }
        if (allX) {
          return true;
        }
      }
    }
  }
  function calcScore(board) {
    let total = 0;
    for (let i = 0; i < board[0].length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        if (board[i][j] != "X") {
          total += board[i][j];
        }
      }
    }
    return total;
  }

  for (let call of myInput.calls) {
    callOut(call);
    console.log({ call });
    for (let b of myInput.boards) {
      if (isWinner(b)) {
        return [b, calcScore(b), call, calcScore(b) * call];
      }
    }
    console.log(myInput.boards);
  }
}


function _ANSWER_2(input)
{
  let myInput = JSON.parse(JSON.stringify(input));
  function callOut(call) {
    for (let b of myInput.boards) {
      for (let br of b) {
        for (let i = 0; i < br.length; i++) {
          if (br[i] == call) {
            br[i] = "X";
          }
        }
      }
    }
  }
  function getIndices(i, n, max, mode) {
    if (mode == "row") {
      return { x: i, y: n };
    } else if (mode == "col") {
      return { x: n, y: i };
    } else if (mode == "diag1") {
      return { x: n, y: n };
    } else if (mode == "diag2") {
      return { x: max - n - 1, y: n };
    }
  }
  function isWinner(board) {
    let modes = ["row", "col"];
    for (let m of modes) {
      for (let i = 0; i < board[0].length; i++) {
        if ((m == "diag1" || m == "diag2") && i > 0) {
          break;
        }
        let allX = true;
        for (let n = 0; n < board[0].length; n++) {
          let indices = getIndices(i, n, board[0].length, m);
          if (board[indices.x][indices.y] != "X") {
            allX = false;
          }
        }
        if (allX) {
          return true;
        }
      }
    }
  }
  function calcScore(board) {
    let total = 0;
    for (let i = 0; i < board[0].length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        if (board[i][j] != "X") {
          total += board[i][j];
        }
      }
    }
    return total;
  }

  let numWon = 0;
  let hasWon = {};

  for (let call of myInput.calls) {
    callOut(call);
    console.log({ call });
    for (let i = 0; i < myInput.boards.length; i++) {
      let b = myInput.boards[i];
      if (isWinner(b)) {
        if (hasWon[i]) {
          continue;
        }
        numWon++;
        hasWon[i] = true;
        console.log("win", i, b, numWon);
        if (numWon == myInput.boards.length) {
          return [b, calcScore(b), call, calcScore(b) * call];
        }
      }
    }
    console.log(myInput.boards);
  }
}



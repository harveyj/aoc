module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 11!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  return inLine.split("").map((a) => a * 1);
}
)}

function _iterGrid(gridFlash){return(
function (grid) {
  for (let y = 0; y < grid.length; y++) {
    for (let x = 0; x < grid[0].length; x++) {
      grid[y][x] += 1;
    }
  }
  let dirty = false;
  do {
    dirty = false;
    for (let y = 0; y < grid.length; y++) {
      for (let x = 0; x < grid[0].length; x++) {
        if (grid[y][x] >= 10) {
          gridFlash(x, y, grid);
          grid[y][x] = -10;
          dirty = true;
        }
      }
    }
  } while (dirty);
  for (let y = 0; y < grid.length; y++) {
    for (let x = 0; x < grid[0].length; x++) {
      if (grid[y][x] < 0) {
        grid[y][x] = 0;
      }
    }
  }
  return grid;
}
)}

function _gridFlash(){return(
function (x, y, grid) {
  let DXDY = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
  ];
  for (let [dx, dy] of DXDY) {
    let nx = x + dx;
    let ny = y + dy;
    if (nx < 0 || ny < 0 || nx >= grid[0].length || ny >= grid.length) {
      continue;
    }
    grid[ny][nx] += 1;
  }
}
)}

function _ANSWER_1(input,iterGrid)
{
  let grid = JSON.parse(JSON.stringify(input));
  let totalFlashes = 0;
  for (let i = 0; i < 100; i++) {
    grid = iterGrid(grid);
    for (let y = 0; y < grid.length; y++) {
      for (let x = 0; x < grid[0].length; x++) {
        if (grid[y][x] != 0) {
          totalFlashes++;
        }
      }
    }
  }
  return totalFlashes;
}


function _ANSWER_2(input,iterGrid)
{
  let grid = JSON.parse(JSON.stringify(input));
  for (let i = 0; i < 1000; i++) {
    grid = iterGrid(grid);
    let allFlash = true;
    for (let y = 0; y < grid.length; y++) {
      for (let x = 0; x < grid[0].length; x++) {
        if (grid[y][x] != 0) {
          allFlash = false;
        }
      }
    }
    if (allFlash) {
      return i + 1;
    }
  }
  return 0;
}



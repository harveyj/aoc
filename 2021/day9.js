module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 9!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split("");
  vals = vals.map((a) => a * 1);
  return vals;
}
)}

function _getNeighborHeight(){return(
function (x, y, grid) {
  if (x < 0 || y < 0 || x >= grid[0].length || y >= grid.length) {
    return 9;
  }
  return grid[y][x];
}
)}

function _ANSWER_1(input,getNeighborHeight)
{
  let grid = input;
  let DXDY = [
    [-1, 0],
    [0, -1],
    [1, 0],
    [0, 1]
  ];
  let mins = [];
  for (let x = 0; x < grid[0].length; x++) {
    for (let y = 0; y < grid.length; y++) {
      let min = true;
      let height = getNeighborHeight(x, y, grid);
      for (let [dx, dy] of DXDY) {
        if (getNeighborHeight(x + dx, y + dy, grid) <= height) {
          min = false;
        }
      }
      if (min) {
        mins.push([x, y]);
      }
    }
  }
  return mins
    .map((a) => getNeighborHeight(a[0], a[1], grid) + 1)
    .reduce((a, b) => a + b);
  return mins;
}


function _ANSWER_2(input,getNeighborHeight)
{
  let grid = input;
  let DXDY = [
    [-1, 0],
    [0, -1],
    [1, 0],
    [0, 1]
  ];
  let mins = [];
  for (let x = 0; x < grid[0].length; x++) {
    for (let y = 0; y < grid.length; y++) {
      let min = true;
      let height = getNeighborHeight(x, y, grid);
      for (let [dx, dy] of DXDY) {
        if (getNeighborHeight(x + dx, y + dy, grid) <= height) {
          min = false;
        }
      }
      if (min) {
        mins.push([x, y]);
      }
    }
  }
  let minSizes = new Map();
  for (let min of mins) {
    let basinPoints = new Map();
    let queue = [min];
    let k = (a, b) => a + "|" + b;
    let loc;
    while ((loc = queue.pop())) {
      let key = k(...loc);
      if (basinPoints.has(key)) {
        continue;
      }
      basinPoints.set(key, 1);
      console.log(key);
      for (let [dx, dy] of DXDY) {
        let nx = loc[0] + dx;
        let ny = loc[1] + dy;
        if (getNeighborHeight(nx, ny, grid) != 9) {
          queue.push([nx, ny]);
        }
      }
    }
    minSizes.set(min, basinPoints.size);
  }
  return Array.from(minSizes.values())
    .sort((a, b) => b - a)
    .slice(0, 3)
    .reduce((a, b) => a * b);
}



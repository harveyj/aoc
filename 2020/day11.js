module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 11!`
)}



function _selectedInput(html,inputRaw)
{
  return html`
    <select>
      ${Object.keys(inputRaw).map(
        key => `<option value=${key}>${key}</option>`
      )}
    </select>
 `;
}


function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n').map(a => a.split(''))
)}

function _getNextSeating(getNeighbors){return(
function(oldSeating) {
  let nextSeating = oldSeating.map(a => a.map(b => '.'));
  for (let y = 0; y < oldSeating.length; y++) {
    for (let x = 0; x < oldSeating[y].length; x++) {
      let neighbors = 0;
      let numOccupied = getNeighbors(
        [x, y],
        [oldSeating[y].length, oldSeating.length]
      )
        .map(a => oldSeating[a.y][a.x])
        .reduce((val, a) => (a == "#" ? val + 1 : val), 0);

      if (oldSeating[y][x] == 'L' && numOccupied == 0) {
        nextSeating[y][x] = '#';
      } else if (oldSeating[y][x] == "#" && numOccupied > 3) {
        nextSeating[y][x] = 'L';
      } else {
        nextSeating[y][x] = oldSeating[y][x];
      }
      // nextSeating[y][x] = numOccupied;
    }
  }
  return nextSeating;
}
)}

function _getNextSeating_2(getNeighborInView){return(
function(oldSeating) {
  let nextSeating = oldSeating.map(a => a.map(b => '.'));
  let grid = nextSeating.map(a => a.map(b => '.'));

  for (let y = 0; y < oldSeating.length; y++) {
    for (let x = 0; x < oldSeating[y].length; x++) {
      let neighbors = 0;
      let numOccupied = getNeighborInView(
        [x, y],
        [oldSeating[y].length, oldSeating.length],
        oldSeating
      );
      grid[y][x] = numOccupied;

      if (oldSeating[y][x] == 'L' && numOccupied == 0) {
        nextSeating[y][x] = '#';
      } else if (oldSeating[y][x] == "#" && numOccupied > 4) {
        nextSeating[y][x] = 'L';
      } else {
        nextSeating[y][x] = oldSeating[y][x];
      }
    }
  }
  console.log(oldSeating);
  console.log(grid);
  return nextSeating;
}
)}

function _getNeighbors(){return(
function([x, y], [maxX, maxY]) {
  let neighbors = [];
  if (x > 0 && y > 0) {
    neighbors.push({ x: x - 1, y: y - 1 });
  }
  if (x > 0) {
    neighbors.push({ x: x - 1, y: y });
  }
  if (x > 0 && y < maxY - 1) {
    neighbors.push({ x: x - 1, y: y + 1 });
  }
  if (y > 0) {
    neighbors.push({ x: x, y: y - 1 });
  }
  if (y < maxY - 1) {
    neighbors.push({ x: x, y: y + 1 });
  }
  if (x < maxX - 1 && y > 0) {
    neighbors.push({ x: x + 1, y: y - 1 });
  }
  if (x < maxX - 1) {
    neighbors.push({ x: x + 1, y: y });
  }
  if (x < maxX - 1 && y < maxY - 1) {
    neighbors.push({ x: x + 1, y: y + 1 });
  }
  return neighbors;
}
)}

function _getNeighborInView(){return(
function([startX, startY], [maxX, maxY], grid) {
  let neighbors = 0;
  let DIRS = [
    [-1, 1],
    [1, -1],
    [1, 1],
    [-1, -1],
    [1, 0],
    [-1, 0],
    [0, -1],
    [0, 1]
  ];
  for (let [dx, dy] of DIRS) {
    let x = startX;
    let y = startY;
    while (true) {
      x += dx;
      y += dy;
      if (x < 0 || y < 0 || y > maxY - 1 || x > maxX - 1) {
        break;
      }
      if (grid[y][x] == 'L') {
        break;
      }
      if (grid[y][x] == '#') {
        neighbors++;
        break;
      }
    }
  }
  return neighbors;
}
)}

function _ANSWER_1(input,getNextSeating)
{
  let oldSeating = input;
  for (let i = 0; i < 10000; i++) {
    let nextSeating = getNextSeating(oldSeating);
    if (JSON.stringify(nextSeating) == JSON.stringify(oldSeating)) {
      let rowTotals = nextSeating.map(row =>
        row.reduce((val, a) => (a == "#" ? val + 1 : val), 0)
      );
      let total = rowTotals.reduce((val, a) => val + a);
      return total;
    }
    oldSeating = nextSeating;
  }
}


function _TEST_1(input,getNextSeating)
{
  let oldSeating = input;
  let frames = [];
  for (let i = 0; i < 10000; i++) {
    let nextSeating = getNextSeating(oldSeating);
    if (JSON.stringify(nextSeating) == JSON.stringify(oldSeating)) {
      let rowTotals = nextSeating.map(row =>
        row.reduce((val, a) => (a == "#" ? val + 1 : val), 0)
      );
      let total = rowTotals.reduce((val, a) => val + a);
      return [i, total, frames];
    }
    oldSeating = nextSeating;
    frames.push(nextSeating);
  }
  return frames;
}


function _TEST(getNeighbors){return(
[
  getNeighbors([0, 0], [3, 3]),
  getNeighbors([1, 1], [3, 3]),
  getNeighbors([1, 2], [3, 3])
]
)}

function _ANSWER_2(input,getNextSeating_2)
{
  let oldSeating = input;
  for (let i = 0; i < 10000; i++) {
    let nextSeating = getNextSeating_2(oldSeating);
    if (JSON.stringify(nextSeating) == JSON.stringify(oldSeating)) {
      let rowTotals = nextSeating.map(row =>
        row.reduce((val, a) => (a == "#" ? val + 1 : val), 0)
      );
      let total = rowTotals.reduce((val, a) => val + a);
      return total;
    }
    oldSeating = nextSeating;
  }
}


function _TEST_2(input,getNextSeating_2,getNeighborInView)
{
  let grid = input.map(a => a.map(b => '.'));
  let seating = getNextSeating_2(input);
  for (let y = 0; y < seating.length; y++) {
    for (let x = 0; x < seating[y].length; x++) {
      grid[y][x] = getNeighborInView(
        [x, y],
        [seating[y].length, seating.length],
        seating
      );
    }
  }
  return grid;
}



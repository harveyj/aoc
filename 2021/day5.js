module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 5!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split(" -> ");
  let start = vals[0].split(",").map((a) => a * 1);
  let end = vals[1].split(",").map((a) => a * 1);
  start = { x: start[0], y: start[1] };
  end = { x: end[0], y: end[1] };
  return { start, end };
}
)}

function _ANSWER_1(input)
{
  function incDefault(map, key) {
    if (!map.has(key)) {
      map.set(key, 0);
    }
    map.set(key, map.get(key) + 1);
  }
  function k(x, y) {
    return x + "," + y;
  }
  let overlaps = new Map();
  for (let line of input) {
    if (line.start.x == line.end.x) {
      for (let y = line.start.y; y <= line.end.y; y++) {
        incDefault(overlaps, k(line.start.x, y));
      }
      for (let y = line.end.y; y <= line.start.y; y++) {
        incDefault(overlaps, k(line.start.x, y));
      }
    } else if (line.start.y == line.end.y) {
      for (let x = line.start.x; x <= line.end.x; x++) {
        incDefault(overlaps, k(x, line.start.y));
      }
      for (let x = line.end.x; x <= line.start.x; x++) {
        incDefault(overlaps, k(x, line.start.y));
      }
    } 
  }
  let overlapCount = 0;
  for (const [key, value] of overlaps.entries()) {
    if (value > 1) {
      overlapCount += 1;
    }
  }
  return overlapCount;
}


function _ANSWER_2(input)
{
  function incDefault(map, key) {
    if (!map.has(key)) {
      map.set(key, 0);
    }
    map.set(key, map.get(key) + 1);
  }
  function k(x, y) {
    return x + "," + y;
  }
  let overlaps = new Map();
  for (let line of input) {
    if (line.start.x == line.end.x) {
      for (let y = line.start.y; y <= line.end.y; y++) {
        incDefault(overlaps, k(line.start.x, y));
      }
      for (let y = line.end.y; y <= line.start.y; y++) {
        incDefault(overlaps, k(line.start.x, y));
      }
    } else if (line.start.y == line.end.y) {
      for (let x = line.start.x; x <= line.end.x; x++) {
        incDefault(overlaps, k(x, line.start.y));
      }
      for (let x = line.end.x; x <= line.start.x; x++) {
        incDefault(overlaps, k(x, line.start.y));
      }
    } else {
      // diagonal
      let delta = Math.abs(line.start.x - line.end.x);
      let dx = line.start.x < line.end.x ? 1 : -1;
      let dy = line.start.y < line.end.y ? 1 : -1;

      for (let i = 0; i <= delta; i++) {
        incDefault(overlaps, k(line.start.x + i * dx, line.start.y + i * dy));
      }
    }
  }
  let overlapCount = 0;
  for (const [key, value] of overlaps.entries()) {
    if (value > 1) {
      overlapCount += 1;
    }
  }
  return overlapCount;
}



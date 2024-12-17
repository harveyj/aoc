// https://observablehq.com/@harveyj/advent-2019-day-3@227
import define1 from "./dea0d0ec849491a6@513.js";

module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2019 Day 3`
)}






function _lines(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n').map(a => a.split(','))
)}

function _DIRS(){return(
{ R: [1, 0], U: [0, 1], D: [0, -1], L: [-1, 0] }
)}

function _grid(DIRS,key){return(
function(input) {
  let grid = new Map();
  let intersects = new Map();
  let steps = 0;
  let debug = [];
  for (let a = 0; a < 2; a++) {
    let steps = 0;
    let [x, y] = [0, 0];
    let inWire = input[a];
    for (let i = 0; i < inWire.length; i++) {
      let segment = inWire[i];
      let [dx, dy] = DIRS[segment[0]];
      for (let j = 0; j < segment.substring(1) * 1; j++) {
        steps += 1;
        x += dx;
        y += dy;
        if (grid.has(key([x, y])) && grid.get(key([x, y])).a != a) {
          let defVal = [grid.get(key([x, y])).steps];
          let vals = intersects.get(key([x, y])) || defVal;
          vals.push(steps);
          intersects.set(key([x, y]), vals);
        }
        grid.set(key([x, y]), { x, y, a, steps });
      }
    }
  }
  return { grid, intersects, debug };
}
)}

function _key(){return(
JSON.stringify
)}

function _manhattan(){return(
function([x, y]) {
  return Math.abs(x) + Math.abs(y);
}
)}

function _out(grid,lines){return(
grid(lines)
)}

function _data(out){return(
Array.from(out.grid.values())
)}

function _ANSWER_2(out,manhattan){return(
Math.min(...Array.from(out.intersects.values()).map(manhattan))
)}

function _ANSWER_1(out,manhattan){return(
Math.min(
  ...Array.from(out.intersects.keys())
    .map(JSON.parse)
    .map(manhattan)
)
)}


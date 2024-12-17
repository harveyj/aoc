module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 12!`
)}






function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput]
  .split('\n')
  .map(a => ({ op: a[0], mag: a.substring(1) * 1 }))
)}

function _DIRS(){return(
[{ x: 1, y: 0 }, { x: 0, y: 1 }, { x: -1, y: 0 }, { x: 0, y: -1 }]
)}

function _ANSWER_1(DIRS,input)
{
  let dirIdx = 0;
  let dir = DIRS[dirIdx];
  let x = 0;
  let y = 0;
  let locs = [];
  for (let inst of input) {
    switch (inst.op) {
      case 'F':
        x += dir.x * inst.mag;
        y += dir.y * inst.mag;
        break;
      case 'N':
        y -= inst.mag;
        break;
      case 'S':
        y += inst.mag;
        break;
      case 'E':
        x += inst.mag;
        break;
      case 'W':
        x -= inst.mag;
        break;
      case 'R':
        dirIdx = dirIdx + inst.mag / 90;
        dirIdx %= 4;
        dir = DIRS[dirIdx];
        break;
      case 'L':
        dirIdx = dirIdx + 4 - inst.mag / 90;
        dirIdx %= 4;
        dir = DIRS[dirIdx];
        break;
    }
    locs.push({ x, y });
  }
  return [Math.abs(x) + Math.abs(y), locs];
}


function _ANSWER_2(input)
{
  let x = 0;
  let y = 0;
  let wayX = 10;
  let wayY = -1;
  let rad = 0;
  let newWayX = 0;
  let newWayY = 0; // hoisted under protest
  let locs = [];
  let wp = [];
  for (let inst of input) {
    switch (inst.op) {
      case 'F':
        x += wayX * inst.mag;
        y += wayY * inst.mag;
        break;
      case 'N':
        wayY -= inst.mag;
        break;
      case 'S':
        wayY += inst.mag;
        break;
      case 'E':
        wayX += inst.mag;
        break;
      case 'W':
        wayX -= inst.mag;
        break;
      case 'R':
        rad = (inst.mag * Math.PI) / 180;
        newWayX = Math.cos(rad) * wayX - Math.sin(rad) * wayY;
        newWayY = Math.sin(rad) * wayX + Math.cos(rad) * wayY;
        wayX = newWayX;
        wayY = newWayY;
        break;
      case 'L':
        rad = ((360 - inst.mag) * Math.PI) / 180;
        newWayX = Math.cos(rad) * wayX - Math.sin(rad) * wayY;
        newWayY = Math.sin(rad) * wayX + Math.cos(rad) * wayY;
        wayX = newWayX;
        wayY = newWayY;
        break;
    }
    locs.push({ x, y });
    wp.push({ wayX, wayY });
  }
  return [Math.abs(x) + Math.abs(y), locs, wp];
}


function _TEST_2()
{
}



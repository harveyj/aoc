module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 2!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split(" ");
  vals[1] = 1 * vals[1];
  return vals;
}
)}

function _ANSWER_1(input)
{
  let depth = 0;
  let forward = 0;
  for (let val of input) {
    let dir = val[0];
    let mag = val[1];
    if (dir == "up") {
      depth -= mag;
    } else if (dir == "down") {
      depth += mag;
    } else if (dir == "forward") {
      forward += mag;
    }
  }
  return depth * forward;
}


function _ANSWER_2(input)
{
  let depth = 0;
  let aim = 0;
  let forward = 0;
  for (let val of input) {
    let dir = val[0];
    let mag = val[1];
    if (dir == "up") {
      aim -= mag;
    } else if (dir == "down") {
      aim += mag;
    } else if (dir == "forward") {
      forward += mag;
      depth += aim * mag;
    }
  }
  return depth * forward;
}



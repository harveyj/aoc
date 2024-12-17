module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 1!`
)}






function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split("\n").map((a) => a * 1)
)}

function _ANSWER_1(input)
{
  let last = 1000000000000;
  let ret = 0;
  for (let a in input) {
    let val = input[a];
    if (val > last) {
      ret += 1;
    }
    last = val;
  }
  return ret;
}


function _ANSWER_2(input)
{
  let queue = [input[0], input[1], input[2]];
  let total = input[0] + input[1] + input[2];
  let lastTotal = total + 1;
  let ret = 0;
  for (let val of input.slice(3)) {
    console.log(val, total, lastTotal);
    queue.push(val);
    total += val;
    total -= queue.shift();
    if (total > lastTotal) {
      ret += 1;
    }
    lastTotal = total;
  }
  return ret;
}



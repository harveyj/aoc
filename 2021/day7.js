module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 7!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)[0]
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split(",");
  vals = vals.map((a) => 1 * a);
  return vals;
}
)}

function _ANSWER_1(input)
{
  let crabs = JSON.parse(JSON.stringify(input));
  crabs = crabs.sort(function (a, b) {
    return a - b;
  });
  let median = crabs[crabs.length / 2];
  let deltas = [];
  let total = 0;
  for (let crab of input) {
    deltas.push(crab - median);
    total += Math.abs(crab - median);
  }
  return { crabs, median, deltas, total };
}


function _ANSWER_2(input)
{
  let crabs = JSON.parse(JSON.stringify(input));
  let distTotal = 0;
  for (let crab of input) {
    distTotal += crab;
  }
  let mean = Math.round(distTotal / crabs.length);
  mean -= 5;
  let totals = new Map();
  for (let i = 0; i < 10; i++) {
    mean += 1;
    let deltas = [];
    let total = 0;
    for (let crab of input) {
      deltas.push(crab - mean);
      let dist = Math.abs(crab - mean);
      total += (dist * (dist + 1)) / 2;
    }
    totals[mean] = total;
  }
  return { crabs, mean, totals };
}


function _8(){return(
[5, 1, 10, 2, 3, 4].sort()
)}


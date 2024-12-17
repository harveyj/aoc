module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 6!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)[0]
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split(",").map((a) => 1 * a);
  return vals;
}
)}

function _repro(){return(
function (fish, life) {
  let newFish = [];
  let appendedFish = [];
  for (let f of fish) {
    if (f > 0) {
      newFish.push(f - 1);
    } else if (f == 0) {
      newFish.push(life - 1);
      appendedFish.push(life + 1);
    }
  }
  newFish = newFish.concat(appendedFish);
  return newFish;
}
)}

function _numFishExpensive(repro){return(
function (fish, life, iters) {
  for (let i = iters; i >= 0; i--) {
    console.log("slow" + (iters - i) + " " + fish.length);
    fish = repro(fish, life);
  }
  return fish.length;
}
)}

function _numFishCheap(){return(
function (fish, life, iters) {
  let total = 0;

  // the starting one cycles = 1
  // it produces another after 7 cycles
  // 1 + f(n-7) + f(n-9)
  let dict = new Map();
  dict[0] = 1;
  dict[1] = 2;
  dict[2] = 2;
  dict[3] = 2;
  dict[4] = 2;
  dict[5] = 2;
  dict[6] = 2;
  dict[7] = 2;
  dict[8] = 3;
  dict[9] = 3;
  for (let i = 10; i <= iters; i++) {
    dict[i] = dict[i - 7] + dict[i - 9];
    console.log("fast" + i + " " + dict[i]);
  }
  return dict[iters];
}
)}

function _ANSWER_1(input,repro)
{
  let iters = 80;
  let life = 7;
  let fish = JSON.parse(JSON.stringify(input))[0];
  fish = [3];
  for (let i = iters; i >= 0; i--) {
        fish = repro(fish, life);
  }
  return fish;
}


function _ANSWER_2(input,numFishCheap)
{
  let iters = 256;
  let life = 7;
  let total = 0;
  for (let i of input) {
    let thisFish = numFishCheap([0], life, iters - i);
    console.log(i, thisFish);
    total += thisFish;
  }
  return { total };
}



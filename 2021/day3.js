module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 3!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  return inLine;
}
)}

function _ANSWER_1(input)
{
  let onesCount = [];
  for (let i = 0; i < input[0].length; i++) {
    onesCount.push(0);
    for (let j = 0; j < input.length; j++) {
      if (input[j][i] == "1") {
        onesCount[i]++;
      }
    }
  }
  let gamma = "0b";
  let epsilon = "0b";
  for (let i = 0; i < onesCount.length; i++) {
    if (onesCount[i] > input.length / 2) {
      gamma += "1";
      epsilon += "0";
    } else {
      epsilon += "1";
      gamma += "0";
    }
  }
  return eval(gamma) * eval(epsilon);
}


function _ANSWER_2(input)
{
  function filterValues(input, i, mcv) {
    let onesCount = 0;
    for (let j = 0; j < input.length; j++) {
      if (input[j][i] == "1") {
        onesCount++;
      }
    }
    let filterVal = "0";
    if (
      (mcv && onesCount >= input.length / 2) ||
      (!mcv && onesCount < input.length / 2)
    ) {
      filterVal = "1";
    }

    let newInput = [];
    for (let j = 0; j < input.length; j++) {
      if (input[j][i] == filterVal) {
        newInput.push(input[j]);
      }
    }
    return newInput;
  }
  let oxygen = 0;
  let newInput = input;
  for (let i = 0; i < input[0].length; i++) {
    newInput = filterValues(newInput, i, true);
    console.log(newInput);
    if (newInput.length == 1) {
      oxygen = eval("0b" + newInput[0]);
      break;
    }
  }
  let scrubber = 0;
  newInput = input;
  for (let i = 0; i < input[0].length; i++) {
    newInput = filterValues(newInput, i, false);
    console.log(newInput);
    if (newInput.length == 1) {
      scrubber = eval("0b" + newInput[0]);
      break;
    }
  }
  return scrubber * oxygen;
}



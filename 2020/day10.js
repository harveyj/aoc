module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _input(INPUT){
  return(
INPUT
  .split('\n')
  .map(a => a * 1)
  .sort((a, b) => a - b)
)}

function _ANSWER_1(inputAdjusted)
{
  let totalOnes = 0;
  let totalThrees = 0;
  inputAdjusted = [0, ...inputAdjusted, inputAdjusted[inputAdjusted.length-1] + 3];
  for (let i = 1; i < inputAdjusted.length; i++) {
    if (inputAdjusted[i] - inputAdjusted[i - 1] == 1) {
      totalOnes++;
    }
    if (inputAdjusted[i] - inputAdjusted[i - 1] == 3) {
      totalThrees++;
    }
  }
  return totalOnes * (totalThrees);
}


function _ANSWER_2(inputAdjusted)
{
  let paths = {};
  inputAdjusted = [0, ...inputAdjusted, inputAdjusted[inputAdjusted.length-1] + 3];
  paths[inputAdjusted.length - 1] = 1;
  for (let i = inputAdjusted.length - 2; i >= 0; i--) {
    let jolt = inputAdjusted[i];
    paths[i] = 0;
    for (let j = i + 1; j < inputAdjusted.length && j < i + 4; j++) {
      let otherJolt = inputAdjusted[j];
      if (otherJolt && otherJolt - jolt < 4) {
        paths[i] += paths[j];
      }
    }
  }
  return paths[0];
}

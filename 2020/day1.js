// https://observablehq.com/@harveyj/advent-2020-day-1@30

function _input(INPUT){return(
  INPUT.split('\n').map(a => 1 * a)
)}

function _ANSWER_1(input)
{
  for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < input.length; j++) {
      if (input[i] + input[j] === 2020) {
        return input[i] * input[j];
      }
    }
  }
}


function _ANSWER_2(input)
{
  for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < input.length; j++) {
      for (let k = 0; k < input.length; k++) {
        if (input[i] + input[j] + input[k] === 2020) {
          return input[i] * input[j] * input[k];
        }
      }
    }
  }
}

module.exports = { _input, _ANSWER_1, _ANSWER_2
};

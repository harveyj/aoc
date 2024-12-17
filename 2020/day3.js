module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 3!`
)}

function _input(INPUT){return(
INPUT.split('\n').map(a => a.split(''))
)}

function _ANSWER_1(input)
{
  let total = 0;
  for (let i = 0; i < input.length; i++) {
    let row = input[i];
    if (row[(i * 3) % row.length] == '#') {
      total += 1;
    }
  }
  return total;
}


function _increments(){return(
[[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
)}

function _ANSWER_2(increments,INPUT)
{
  let results = [];
  for (let a = 0; a < increments.length; a++) {
    let total = 0;
    let [dx, dy] = increments[a];
    for (let i = 0; i < INPUT.length / dy; i++) {
      let row = INPUT[i * dy];
      // results.push('.');
      if (row[(i * dx) % row.length] == '#') {
        total += 1;
      }
    }
    results.push(total);
  }
  // return results;
  return results.reduce((a, b) => a * b);
}



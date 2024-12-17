module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 5!`
)}






function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n')
)}

function _toId(){return(
function(input) {
  let row = 0;
  let increment = 64;
  for (let i = 0; i < 7; i++) {
    if (input[i] === 'B') {
      row += increment;
    }
    increment /= 2;
  }
  let col = 0;
  increment = 4;
  for (let i = 7; i < 10; i++) {
    if (input[i] === 'R') {
      col += increment;
    }
    increment /= 2;
  }
  return row * 8 + col;
}
)}

function _ids(input,toId){return(
input.map(toId)
)}

function _sortedIds(ids){return(
ids.sort()
)}

function _ANSWER_1(ids){return(
Math.max(...ids)
)}

function _ANSWER_2(sortedIds)
{
  let answer = [];
  for (let i = 1; i < sortedIds.length - 1; i++) {
    if (sortedIds[i - 1] != sortedIds[i] - 1) {
      answer.push(sortedIds[i - 1] + 1);
    }
  }
  return answer;
}



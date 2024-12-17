module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 2!`
)}

function _input(INPUT){return(
INPUT.split('\n').map(parseInstruction)
)}

function parseInstruction(){return(
function(val) {
  let [full, min, max, letter, password] = val.match(/(\d+)-(\d+) (\w): (\w+)/);
  return { min, max, letter, password };
}
)}

function _ANSWER_1(input)
{
  let matches = 0;
  console.log(input);
  for (let i = 0; i < input.length; i++) {
    let pwObj = input[i];
    let count = (pwObj.password.match(new RegExp(pwObj.letter, 'g')) || [])
      .length;
    if (pwObj.min * 1 <= count && count <= pwObj.max * 1) {
      matches += 1;
    }
    // return [pwObj.min * 1, count, pwObj.max * 1];
  }
  return matches;
}


function _ANSWER_2(input)
{
  let matches = 0;
  for (let i = 0; i < input.length; i++) {
    let pwObj = input[i];
    let c1 = pwObj.password[pwObj.min - 1];
    let c2 = pwObj.password[pwObj.max - 1];
    if ((c1 == pwObj.letter || c2 == pwObj.letter) && !(c1 == c2)) {
      matches += 1;
    }
  }
  return matches;
}


function _8(){return(
'cccc'.match(new RegExp('c', 'g'))
)}


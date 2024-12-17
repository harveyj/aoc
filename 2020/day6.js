module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 6!`
)}






function _input(INPUT){return(
INPUT.split('\n\n').map(a => a.split('\n'))
)}

function _ANSWER_1(input)
{
  let total = 0;
  for (let i = 0; i < input.length; i++) {
    let group = input[i];
    let items = new Map();
    for (let j = 0; j < group.length; j++) {
      let person = group[j];
      for (let k = 0; k < person.length; k++) {
        items.set(person[k], true);
      }
    }
    total += items.size;
  }
  return total;
}


function _ANSWER_2(input)
{
  let total = 0;
  for (let i = 0; i < input.length; i++) {
    let group = input[i];
    let items = new Map();
    for (let j = 0; j < group.length; j++) {
      let person = group[j];
      for (let k = 0; k < person.length; k++) {
        items.set(person[k], (items.get(person[k]) || 0) + 1);
      }
    }
    for (let [item, value] of items.entries()) {
      console.log([value, group.length]);
      if (value === group.length) {
        console.log('yes');

        total += 1;
      }
    }
  }
  return total;
}


function _results(){return(
[
]
)}


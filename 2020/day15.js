module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 15!`
)}



function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split(',').map(a => a * 1)
)}




function _ANSWER_1(input)
{
  let mem = new Map();
  let nums = [];
  let uttered = [];
  for (let i = 0; i < input.length; i++) {
    mem.set(input[i], i + 1);
    uttered.push(input[i]);
  }

  for (let i = input.length; i < 30000000; i++) {
    let turn = i + 1;
    let last = uttered[uttered.length - 1];
    if (!mem.has(last)) {
      uttered.push(0);
    } else {
      uttered.push(i - mem.get(last));
    }
    mem.set(last, i);
  }
  return uttered[uttered.length - 1];
}


function _setCharAt(){return(
function setCharAt(str, index, chr) {
  if (index > str.length - 1) return str;
  return str.substring(0, index) + chr + str.substring(index + 1);
}
)}


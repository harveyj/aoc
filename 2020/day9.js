module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 9!`
)}



function _selectedInput(html,inputRaw)
{
  return html`
    <select>
      ${Object.keys(inputRaw).map(
        key => `<option value=${key}>${key}</option>`
      )}
    </select>
 `;
}


function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n').map(a => a * 1)
)}

function _ANSWER_1(input)
{
  let PREAMBLE = 25;
  let window = [];
  for (let i = 0; i < PREAMBLE; i++) {
    window.push(input[i]);
  }
  for (let i = PREAMBLE; i < input.length; i++) {
    let newVal = input[i];
    let allSums = new Set();
    for (let j = 0; j < window.length; j++) {
      for (let k = 0; k < window.length; k++) {
        if (j != k) {
          allSums.add(window[j] + window[k]);
        }
      }
    }
    if (!allSums.has(newVal)) {
      return newVal;
    }
    window.shift();
    window.push(newVal);
  }
}


function _RANGE_2(input)
{
  let TARGET = 257342611;
  // let TARGET = 127;
  let start = 0;
  let end = 0;
  let total = input[start];
  while (end < input.length) {
    while (total < TARGET) {
      end += 1;
      total += input[end];
    }
    if (total == TARGET) {
      return [start, end];
    } else {
      total -= input[end];
      end--;
      total -= input[start];
      start++;
    }
  }
}


function _ANSWER_2(RANGE_2,input)
{
  let max = 0;
  let min = 100000000000000;
  for (let i = RANGE_2[0]; i < RANGE_2[1]; i++) {
    if (input[i] < min) {
      min = input[i];
    }
    if (input[i] > max) {
      max = input[i];
    }
  }
  return min + max;
}



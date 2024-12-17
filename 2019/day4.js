module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2019 Day 4`
)}

function _start(){return(
356261
)}

function _end(){return(
846303
)}

function _legals(start,end)
{
  let legalsFirst = [];
  let legalsSecond = [];
  let ascending = function(val) {
    let last = 10;
    while (val > 0) {
      let digit = val % 10;
      if (digit > last) {
        return false;
      }
      last = digit;
      val = Math.floor(val / 10);
    }
    return true;
  };
  let double = function(val) {
    let last = NaN;
    while (val > 0) {
      let digit = val % 10;
      if (digit === last) {
        return true;
      }
      last = digit;
      val = Math.floor(val / 10);
    }
    return false;
  };
  let onlyDouble = function(val) {
    let doubles = new Map();
    let last = NaN;
    while (val > 0) {
      let digit = val % 10;
      if (digit === last) {
        if (doubles.get(digit) === 1 || doubles.get(digit) === 2) {
          doubles.set(digit, 2);
        } else {
          doubles.set(digit, 1);
        }
      }
      last = digit;
      val = Math.floor(val / 10);
    }
    return Array.from(doubles.values()).indexOf(1) !== -1;
  };
  for (let i = start; i < end; i++) {
    if (ascending(i) && double(i)) {
      legalsFirst.push(i);
    }
    if (ascending(i) && onlyDouble(i)) {
      legalsSecond.push(i);
    }
  }
  return { legalsFirst, legalsSecond };
}



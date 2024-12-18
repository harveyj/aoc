module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 16!`
)}



function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(processNearby,processSpecs){return(
function(input) {
  let nearby = input
    .split("nearby tickets:\n")[1]
    .split('\n')
    .map(processNearby);
  let specs = input
    .split("your ticket:")[0]
    .split('\n')
    .map(processSpecs)
    .filter(a => a);
  return { nearby, specs };
}
)}

function _processSpecs(){return(
function(item) {
  if (!item) {
    return;
  }
  let name = item.split(':')[0];
  let vals = item.split(':')[1];
  vals = vals.split('or').map(a => {
    let match = a.match(/(\d+)-(\d+)/);
    return { a: match[1] * 1, b: match[2] * 1 };
  });
  return { name, vals };
}
)}

function _processNearby(){return(
function(item) {
  return item.split(',').map(a => a * 1);
}
)}




function _ANSWER_1(input)
{
  function valueInvalid(field) {
    for (let spec of input.specs) {
      for (let val of spec.vals) {
        if (val.a <= field && val.b >= field) {
          return false;
        }
      }
    }
    return true;
  }

  let bustedTickets = 0;
  let bustedValues = [];
  let goodTickets = [];
  for (let i = 0; i < input.nearby.length; i++) {
    let tick = input.nearby[i];
    let valid = true;
    for (let field of tick) {
      if (valueInvalid(field)) {
        bustedTickets++;
        bustedValues.push(field);
        valid = false;
        break;
      }
    }
    if (valid) {
      goodTickets.push(tick);
    }
  }
  return {
    answer: bustedValues.reduce((a, b) => a + b, 0),
    bustedValues,
    goodTickets
  };
}


function _ANSWER_2(ANSWER_1,input)
{
  function invalidForValue(spec, value) {
    let found = true;
    for (let i = 0; i < spec.vals.length; i++) {
      let val = spec.vals[i];
      if (val.a <= value && val.b >= value) {
        // console.log('found');
        found = false;
      }
    }
    return found;
  }

  let invalids = new Map();
  let TICK_LEN = ANSWER_1.goodTickets[0].length;
  for (let i = 0; i < TICK_LEN; i++) {
    invalids.set(i, new Set());
    for (let tick of ANSWER_1.goodTickets) {
      let field = tick[i];
      for (let spec of input.specs) {
        if (invalidForValue(spec, field)) {
          // console.log(spec, field, tick, i);
          invalids.get(i).add(spec.name);
        }
      }
    }
  }
  let answers = new Map();
  let log = [];
  for (let i = 0; i < 1000; i++) {
    for (let spec of input.specs) {
      invalids.forEach((val, key) => {
        if (val.size == input.specs.length - 1 && !val.has(spec.name)) {
          answers[spec.name] = key;
          invalids.forEach((val, key) => val.add(spec.name));
        }
      });
    }
  }
  return { answers, log, invalids };
}


function _tick(){return(
[
  73,
  59,
  83,
  127,
  137,
  151,
  71,
  139,
  67,
  53,
  89,
  79,
  61,
  109,
  131,
  103,
  149,
  97,
  107,
  101
]
)}

function _11(tick){return(
tick[11] * tick[4] * tick[5] * tick[0] * tick[18] * tick[8]
)}

function _setCharAt(){return(
function setCharAt(str, index, chr) {
  if (index > str.length - 1) return str;
  return str.substring(0, index) + chr + str.substring(index + 1);
}
)}


module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 13!`
)}

function _input(INPUT){
return INPUT.split('\n');
}

function processInput(input)
{
  return { start: input[0] * 1, periods: input[1].split(',').map(a => 1 * a) };
}


function _ANSWER_1(input)
{
  let processedInput = processInput(input);
  let bestBus = null;
  let bestGap = 10000000000000000;
  let gaps = {};
  for (let i = 0; i < processedInput.periods.length; i++) {
    let bus = processedInput.periods[i];
    if (!bus) {
      continue;
    }
    let nextTime = Math.ceil(processedInput.start / bus) * bus;
    let gap = nextTime - processedInput.start;
    if (gap < bestGap) {
      bestGap = gap;
      bestBus = bus;
    }
    gaps[bus] = gap;
  }
  return bestBus * bestGap;
}


function _ANSWER_2(input)
{
  let processedInput = processInput(input);
  let buses = processedInput.periods;
  step = 1;
  val = 0;
  for (i = 0; i < buses.length; i++) {
    while (buses[i]) {
      if ((val + i) % buses[i] == 0) {
        step *= buses[i];
        break;
      }
      val += step;
    }
  }
  return val;
}

function _SLOW_ANSWER_2(input)
{
  let processedInput = processInput(input);
  function findA(busIndex, bus, a, b) {
    for (let i = a; i < 1000000000000000; i += b) {
      if (i % bus == (bus - busIndex) % bus) {
        a = i;
        b *= bus;
        return [a, b];
      }
    }
    return [-1, -1] // error condition
  }
  let vals = [];
  let buses = processedInput.periods;
  let a = 0;
  let b = buses[0];
  for (let busIndex = 1; busIndex < buses.length; busIndex++) {
    let bus = buses[busIndex];
    if (!bus) {
      continue;
    }
    [a, b] = findA(busIndex, bus, a, b);
  }
  return { a, b };
}
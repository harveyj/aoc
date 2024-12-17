module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 13!`
)}



function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n')
)}

function _processedInput(input)
{
  return { start: input[0] * 1, periods: input[1].split(',').map(a => 1 * a) };
}


function _ANSWER_1(processedInput)
{
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
  return { answer: bestBus * bestGap, gaps };
}


// called _SLOW_ANSWER_2
function _ANSWER_2(processedInput)
{
  function findA(busIndex, bus, a, b) {
    for (let i = a; i < 1000000000000000; i += b) {
      if (i % bus == (bus - busIndex) % bus) {
        a = i;
        b *= bus;
        return [a, b];
      }
    }
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
// https://observablehq.com/@harveyj/advent-2019-1@76
module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2019 1`
)}




function _3(md){return(
md`Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

`
)}



function _inputs(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n').map(a => 1 * a)
)}

function _fuelRequired(){return(
function(inval) {
 return Math.floor(inval / 3) - 2
}
)}

function _outs(inputs,fuelRequired){return(
inputs.map(a => fuelRequired(a))
)}

function _sumReducer(){return(
(accumulator, currentValue) => accumulator + currentValue
)}

function _startFuel(outs,sumReducer){return(
outs.reduce(sumReducer)
)}

function _endFuel(fuelRequired){return(
function(startFuel) {
  let fuel = startFuel;
  let endFuel = 0;
  while (fuel > 0) {
    endFuel += fuel;
    fuel = fuelRequired(fuel)
  }
  return endFuel;
}
)}

function _outsAdjusted(outs,endFuel){return(
outs.map(endFuel)
)}

function _12(outsAdjusted,sumReducer){return(
outsAdjusted.reduce(sumReducer)
)}


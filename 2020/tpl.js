function _1(md){return(
md`# Advent 2021 Day N!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split(" ");
  vals[1] = 1 * vals[1];
  return vals;
}
)}

function _ANSWER_1()
{
  return 0;
}


function _ANSWER_2()
{
  return 0;
}


export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("inputRaw")).define("inputRaw", _inputRaw);
  main.variable(observer("viewof selectedInput")).define("viewof selectedInput", ["html","inputRaw"], _selectedInput);
  main.variable(observer("selectedInput")).define("selectedInput", ["Generators", "viewof selectedInput"], (G, _) => G.input(_));
  main.variable(observer("input")).define("input", ["inputRaw","selectedInput","processInput"], _input);
  main.variable(observer("processInput")).define("processInput", _processInput);
  main.variable(observer("ANSWER_1")).define("ANSWER_1", _ANSWER_1);
  main.variable(observer("ANSWER_2")).define("ANSWER_2", _ANSWER_2);
  return main;
}

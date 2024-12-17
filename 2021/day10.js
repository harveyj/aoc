module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 10!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  return inLine;
}
)}

function _ANSWER_1(input)
{
  let START_CHARS = ["(", "[", "{", "<"];
  let END_CHARS = [")", "]", "}", ">"];
  let corrupted = [];
  let incomplete = [];

  let complement = new Map();
  complement.set("{", "}");
  complement.set("(", ")");
  complement.set("[", "]");
  complement.set("<", ">");
  complement.set("}", "{");
  complement.set(")", "(");
  complement.set("]", "[");
  complement.set(">", "<");

  let badScore = new Map();
  badScore.set(")", 3);
  badScore.set("]", 57);
  badScore.set("}", 1197);
  badScore.set(">", 25137);

  let total = 0;
  for (let line of input) {
    let expected = [];
    for (let c of line) {
      if (START_CHARS.includes(c)) {
        expected.push(c);
      } else {
        let last = expected.pop();
        if (!last) {
          break;
        }
        if (complement.get(c) != last) {
          console.log("bad", c, badScore.get(c));
          total += badScore.get(c);
          break;
        }
      }
    }
  }
  return total;
}


function _ANSWER_2(input)
{
  let START_CHARS = ["(", "[", "{", "<"];
  let END_CHARS = [")", "]", "}", ">"];
  let corrupted = [];
  let incomplete = [];

  let complement = new Map();
  complement.set("{", "}");
  complement.set("(", ")");
  complement.set("[", "]");
  complement.set("<", ">");
  complement.set("}", "{");
  complement.set(")", "(");
  complement.set("]", "[");
  complement.set(">", "<");

  let badScore = new Map();
  badScore.set(")", 3);
  badScore.set("]", 57);
  badScore.set("}", 1197);
  badScore.set(">", 25137);

  let completeScore = new Map();
  completeScore.set("(", 1);
  completeScore.set("[", 2);
  completeScore.set("{", 3);
  completeScore.set("<", 4);

  let scores = [];
  for (let line of input) {
    let expected = [];
    let bad = false;
    for (let c of line) {
      if (START_CHARS.includes(c)) {
        expected.push(c);
      } else {
        let last = expected.pop();
        if (!last) {
          break;
        }
        if (complement.get(c) != last) {
          bad = true;
          break;
        }
      }
    }
    if (!bad) {
      console.log(line, expected);
      let subTotal = 0;
      let complete;
      while ((complete = expected.pop())) {
        subTotal *= 5;
        subTotal += completeScore.get(complete);
      }
      console.log(subTotal);
      scores.push(subTotal);
    }
  }
  scores = scores.sort((a, b) => a - b);
  // return scores;
  return scores[(scores.length - 1) / 2];
}



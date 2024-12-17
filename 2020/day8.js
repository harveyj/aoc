module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 8!`
)}






function _input(inputRaw,selectedInput,parseInstruction){return(
inputRaw[selectedInput].split('\n').map(parseInstruction)
)}

function _parseInstruction(){return(
function(inst) {
  let instRe = /(...) (.\d+)/;
  let [_, op, val] = inst.match(instRe);
  val *= 1;
  return { op, val };
}
)}

function _run(){return(
function(program) {
  let pc = 0;
  let acc = 0;
  let seenPc = new Set();
  while (pc < program.length) {
    let inst = program[pc];
    if (seenPc.has(pc)) {
      return null;
    } else {
      seenPc.add(pc);
    }
    switch (inst.op) {
      case "nop":
        pc += 1;
        break;
      case "jmp":
        pc += inst.val;
        break;
      case "acc":
        pc += 1;
        acc += inst.val;
        break;
    }
  }
  return acc;
}
)}

function _ANSWER_1(run,input)
{
  return run(input);
}


function _ANSWER_2(input,run)
{
  let program = input;
  for (let i = 0; i < program.length; i++) {
    if (program[i].op == "nop") {
      program[i].op = "jmp";
    } else if (program[i].op == "jmp") {
      program[i].op = "nop";
    }

    let val = run(program);
    if (val !== null) {
      return val;
    }

    if (program[i].op == "nop") {
      program[i].op = "jmp";
    } else if (program[i].op == "jmp") {
      program[i].op = "nop";
    }
  }
}



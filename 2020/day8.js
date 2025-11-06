module.exports = { _input, _ANSWER_1, _ANSWER_2};

function parseInstruction(inst){
    let instRe = /(...) (.\d+)/;
    let [_, op, val] = inst.match(instRe);
    val *= 1;
    return { op, val };
}
  

function _input(input){return(
input.split('\n').map(parseInstruction)
)}


function run(program) {
  let pc = 0;
  let acc = 0;
  let seenPc = new Set();
  while (pc < program.length) {
    let inst = program[pc];
    if (seenPc.has(pc)) {
      return -1 * acc;
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

function _ANSWER_1(input)
{
  return run(input)*-1;
}


function _ANSWER_2(input)
{
  let program = input;
  for (let i = 0; i < program.length; i++) {
    if (program[i].op == "nop") {
      program[i].op = "jmp";
    } else if (program[i].op == "jmp") {
      program[i].op = "nop";
    }

    let val = run(program);
    if (val > 0) {
      return val;
    }

    if (program[i].op == "nop") {
      program[i].op = "jmp";
    } else if (program[i].op == "jmp") {
      program[i].op = "nop";
    }
  }
}



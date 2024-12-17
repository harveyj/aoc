
module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2019 2`
)}






function _program(inputRaw,selectedInput){return(
inputRaw[selectedInput].split(',').map(a => 1 * a)
)}

function _run(){return(
function(program) {
  let pc = 0;
  let debug = [];
  while (pc < program.length) {
    let [a, b, c] = [program[pc + 1], program[pc + 2], program[pc + 3]];
    let [indir_a, indir_b] = [program[a], program[b]];
    debug.push(["op", program[pc]]);
    switch (program[pc]) {
      case 1:
        program[c] = indir_a + indir_b;
        debug.push(c);
        break;
      case 2:
        program[c] = indir_a * indir_b;
        debug.push(c);
        break;
      case 99:
        return [program, debug];
    }
    pc += 4;
  }
  return [program, debug];
}
)}

function _solvePuzzle(program,run)
{
  let lookingFor = 19690720;
  let ret = [];

  // Part 1
  let mutableProgram = JSON.parse(JSON.stringify(program));
  mutableProgram[1] = 12;
  mutableProgram[2] = 2;
  run(mutableProgram);
  // return mutableProgram[0];

  // Part 2
  for (let i = 0; i < 100; i++) {
    for (let j = 0; j < 100; j++) {
      let mutableProgram = JSON.parse(JSON.stringify(program));
      mutableProgram[1] = i;
      mutableProgram[2] = j;
      run(mutableProgram);
      ret.push([i, j, mutableProgram[0], mutableProgram]);
      if (mutableProgram[0] == lookingFor) {
        return mutableProgram, i * 100 + j;
      }
    }
  }
  return ret;
}



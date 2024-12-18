module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 25 - Christmas!`
)}

function _input(input) {
  return processInput(input);
}

function processInput(input) {
  let [publicCard, publicDoor] = input.split('\n').map(a => a * 1);
  return { publicCard, publicDoor };
}

function transform(val, subjectNumber) {
  val *= subjectNumber;
  val = val % 20201227;
  return val;
}

function transformN(subjectNumber, loopSize) {
  let val = 1;
  for (let i = 0; i < loopSize; i++) {
    val = transform(val, subjectNumber);
  }
  return val;
}

function findLoopSize(publicKey, subjectNumber) {
  let MAX = 100000000;
  let val = 1;
  for (let i = 0; i < MAX; i++) {
    val = transform(val, subjectNumber);
    if (val == publicKey) {
      return i + 1;
    }
  }
  return -1;
}

function _ANSWER_1(input)
{
  let loopSize = findLoopSize(input.publicDoor, 7);
  return transformN(input.publicCard, loopSize);
}


function _ANSWER_2()
{
  return 20201225;
}



module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 25 - Christmas!`
)}



function _selectedInput(html,inputRaw)
{
  return html`
    <select>
      ${Object.keys(inputRaw).map(
        key => `<option value=${key}>${key}</option>`
      )}
    </select>
 `;
}


function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(){return(
function(input) {
  let [publicCard, publicDoor] = input.split('\n').map(a => a * 1);
  return { publicCard, publicDoor };
}
)}

function _transform(){return(
function(val, subjectNumber) {
  val *= subjectNumber;
  val = val % 20201227;
  return val;
}
)}

function _transformN(transform){return(
function(subjectNumber, loopSize) {
  let val = 1;
  for (let i = 0; i < loopSize; i++) {
    val = transform(val, subjectNumber);
  }
  return val;
}
)}

function _findLoopSize(transform){return(
function(publicKey, subjectNumber) {
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
)}

function _ANSWER_1(findLoopSize,input,transformN)
{
  let loopSize = findLoopSize(input.publicDoor, 7);
  console.log(loopSize);
  return transformN(input.publicCard, loopSize);
}


function _ANSWER_2()
{
}



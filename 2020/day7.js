module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 7!`
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


function _input(inputRaw,selectedInput){return(
inputRaw[selectedInput].split('\n')
)}

function _processedInput(input)
{
  let tree = new Map();
  let reverseTree = new Map();
  let vals = [];
  for (let line of input) {
    let pat = /(.*) bags contain (.*)/;
    let bagPat = /(\d+) (.*) bag/;
    let [_, container, containeeStr] = line.match(pat);
    let containees = containeeStr.split(',');
    for (let bag of containees) {
      let [_2, num, val] = bag.match(bagPat) || ['', '', ''];
      num *= 1;
      let nodes = tree.get(val) || [];
      nodes.push(container);
      tree.set(val, nodes);

      let reverseNodes = reverseTree.get(container) || [];
      reverseNodes.push({ val, num });
      reverseTree.set(container, reverseNodes);
    }
  }
  return { tree, reverseTree };
}


function _walkTree(processedInput){return(
function(start) {
  let legals = new Set();
  let queue = [start];
  while (queue.length > 0) {
    let val = queue.pop();
    legals.add(val);
    let newNodes = processedInput.tree.get(val) || [];

    for (let node of newNodes) {
      queue.push(node);
    }
  }
  return legals;
}
)}

function _containedBags(processedInput){return(
function(currentBag) {
  let cbHelper = function(currentBag) {
    let children = processedInput.reverseTree.get(currentBag) || [];
    console.log(children, processedInput.reverseTree, currentBag);
    let totalContainedBags = 0;
    for (let child of children) {
      totalContainedBags += cbHelper(child.val) * child.num;
    }

    return 1 + totalContainedBags;
  };
  return cbHelper(currentBag);
}
)}

function _ANSWER_1(walkTree)
{
  return walkTree("shiny gold").size - 1;
}


function _ANSWER_2(containedBags)
{
  return containedBags("shiny gold");
}


function _results(){return(
[
]
)}

function _a()
{
  let z = [5];
  z.pop();
  return z;
}



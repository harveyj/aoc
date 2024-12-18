module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 7!`
)}

function _input(INPUT){return(
INPUT.split('\n')
)}

function processInput(input)
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


function walkTree(processedInput, start){
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

function containedBags(processedInput, currentBag) {
  let cbHelper = function(currentBag) {
    let children = processedInput.reverseTree.get(currentBag) || [];
    let totalContainedBags = 0;
    for (let child of children) {
      totalContainedBags += cbHelper(child.val) * child.num;
    }

    return 1 + totalContainedBags;
  };
  return cbHelper(currentBag);
}

function _ANSWER_1(input)
{
  let processedInput = processInput(input)
  return walkTree(processedInput, "shiny gold").size - 1;
}


function _ANSWER_2(input)
{
  let processedInput = processInput(input)
  return containedBags(processedInput, "shiny gold") - 1;
}


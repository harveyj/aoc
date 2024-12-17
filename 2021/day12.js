module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 12!`
)}






function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(){return(
function (input) {
  let lines = input.split("\n");
  let graph = {};
  let addEdge = function (p1, p2) {
    if (!graph[p1]) {
      graph[p1] = { name: p1, edges: {} };
    }
    if (!graph[p2]) {
      graph[p2] = { name: p2, edges: {} };
    }
    graph[p1].edges[p2] = graph[p2];
    graph[p2].edges[p1] = graph[p1];
  };
  for (let line of lines) {
    let [p1, p2] = line.split("-");
    addEdge(p1, p2);
  }
  return { graph };
}
)}

function _bfs(){return(
function (graph, op) {
  let isLower = (s) => s.toLowerCase() === s;
  let queue = [[[], graph.start]];
  let allPaths = {};
  while (true) {
    let head = queue.pop();
    console.log({ head, queue: Object.assign({}, queue) });
    if (!head) {
      break;
    }
    let [path, node] = head;
    if (node.name == "end") {
      allPaths[JSON.stringify(path)] = true;
      continue;
    }
    if (isLower(node.name)) {
      if (path.includes(node.name)) {
        console.log("seenSmall", node.name);
        continue;
      }
    }
    // console.log(Object.values(node.edges));
    for (let next of Object.values(node.edges)) {
      let newPath = [...path];
      newPath.push(node.name);
      queue.unshift([newPath, next]);
    }
  }
  return Object.keys(allPaths);
}
)}

function _ANSWER_1(bfs,input)
{
  return bfs(input.graph);
}


function _bfs2(){return(
function (graph, op) {
  let isLower = (s) => s.toLowerCase() === s;
  let queue = [[[], null, graph.start]];
  let allPaths = {};
  while (true) {
    let head = queue.pop();
    if (!head) {
      break;
    }
    let [path, singleSmall, node] = head;
    if (node.name == "end") {
      allPaths[JSON.stringify(path)] = true;
      continue;
    }
    if (isLower(node.name)) {
      if (path.includes(node.name)) {
        if (singleSmall) {
          continue;
        }
        singleSmall = node.name;
      }
    }
    if (node.name == "start" && path.length > 0) {
      continue;
    }
    for (let next of Object.values(node.edges)) {
      let newPath = [...path];
      newPath.push(node.name);
      queue.unshift([newPath, singleSmall, next]);
    }
  }
  return Object.keys(allPaths);
}
)}

function _ANSWER_2(bfs2,input)
{
  return bfs2(input.graph);
}



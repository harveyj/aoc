module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _input(input) {
  return processInput(input)
}

function processInput(input) {
  function processGrid(rawGrid) {
    let lines = rawGrid.split('\n');
    let id = lines[0].match(/Tile (\d+)/)[1];
    return [id, new Grid(lines.slice(1))];
  }
  return new Map(input.split('\n\n').map(processGrid));
}

function reverseString (str) {
  let arr = Array.from(str);
  arr.reverse();
  return arr.join('');
}

class Grid {
  constructor(grid, rotation) {
    this.grid = grid;
    this.size = grid.length;
    this.edges = [];
    this.fillEdges();
  }

  fillEdges() {
    let out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.grid[0][i]);
    }
    this.edges.push(out.join(''));
    out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.grid[i][this.size - 1]);
    }
    this.edges.push(out.join(''));
    out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.grid[this.size - 1][this.size - 1 - i]);
    }
    this.edges.push(out.join(''));
    out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.grid[this.size - 1 - i][0]);
    }
    this.edges.push(out.join(''));
    this.edges = this.edges.concat(this.edges.map(reverseString));
  }

  get(x, y, rotation) {
    if (y > this.grid.length - 1 || x > this.grid[y].length - 1) {
      return '';
    }
    if (rotation > 3) {
      rotation -= 4;
      x = this.size - x - 1;
    }
    if (rotation == 0) {
      return this.grid[y][x];
    } else if (rotation == 1) {
      return this.grid[x][this.size - 1 - y];
    } else if (rotation == 2) {
      return this.grid[this.size - 1 - y][this.size - 1 - x];
    } else if (rotation == 3) {
      return this.grid[this.size - 1 - x][y];
    }
  }

  getRightEdge(rotation) {
    let out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.get(this.size - 1, i, rotation));
    }
    return out.join('');
  }

  getLeftEdge(rotation) {
    let out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.get(0, i, rotation));
    }
    return out.join('');
  }

  getTopEdge(rotation) {
    let out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.get(i, 0, rotation));
    }
    return out.join('');
  }

  getBottomEdge(rotation) {
    let out = [];
    for (let i = 0; i < this.size; i++) {
      out.push(this.get(i, this.size - 1, rotation));
    }
    return out.join('');
  }

  matchRight(grid, rotation) {
    let rightEdge = this.getRightEdge(rotation);

    for (let i = 0; i < 8; i++) {
      if (rightEdge === grid.getLeftEdge(i)) {
        return i;
      }
    }
    return -1;
  }

  matchBottom(grid, rotation) {
    let bottomEdge = this.getBottomEdge(rotation);

    for (let i = 0; i < 8; i++) {
      if (bottomEdge === grid.getTopEdge(i)) {
        return i;
      }
    }
    return -1;
  }

  findAlignments(grid) {
    let alignments = [];
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        if (this.edges[i] === grid.edges[j]) {
          alignments.push([i, j]);
        }
      }
    }
    return alignments;
  }

  str(rotation) {
    let rows = [];
    for (let y = 0; y < this.size; y++) {
      let cols = [];
      for (let x = 0; x < this.size; x++) {
        cols.push(this.get(x, y, rotation));
      }
      rows.push(cols.join(''));
    }
    return rows.join('\n');
  }

  trim(rotation) {
    let rows = [];
    for (let y = 1; y < this.size - 1; y++) {
      let cols = [];
      for (let x = 1; x < this.size - 1; x++) {
        cols.push(this.get(x, y, rotation));
      }
      rows.push(cols);
    }
    return rows;
  }

  findMonsters(rotation) {
    let numFound = 0;
    for (let x = 0; x < this.size; x++) {
      for (let y = 0; y < this.size; y++) {
        let allFound = true;
        for (let [moy, mox] of monsterOffsets) {
          if (this.get(x + mox, y + moy, rotation) != '#') {
            allFound = false;
          }
        }
        numFound += allFound ? 1 : 0;
      }
    }
    return numFound;
  }
}

function _ANSWER_1(input)
{
  let cm = connectionMatrix(input);
  let connections = connect(cm);
  return Array.from(connections.corners.keys()).reduce((acc, curr) => acc * curr, 1);
}


function connectionMatrix(input)
{
  let ret = new Map();
  for (let [id, grid] of input.entries()) {
    let row = new Map();
    for (let [id2, grid2] of input.entries()) {
      if (grid == grid2) {
        continue;
      }
      row.set(id2, grid.findAlignments(grid2));
    }
    ret.set(id, row);
  }
  return ret;
}


function connect(connectionMatrix)
{
  let foundTwoConnections = new Map();
  let realConnections = new Map();
  for (let [key, val] of connectionMatrix.entries()) {
    let connections = [];
    for (let key2 of val.keys()) {
      if (val.get(key2).length != 0) {
        connections.push(key2);
      }
    }
    realConnections.set(key, connections);
    if (connections.length == 2) {
      foundTwoConnections.set(key, connections);
    }
  }
  return { corners: foundTwoConnections, realConnections };
}


function genEdges(connect) {
  let start = connect.corners.keys().next().value;
  let topEdge = findEdge(start, connect.corners.get(start)[0]);
  let leftEdge = findEdge(start, connect.corners.get(start)[1]);
  function findEdge(start, next) {
    let from = start;
    let candidate = next;
    let edge = [start];
    while (true) {
      edge.push(candidate);
      let neighborCounts = new Map(
        connect.realConnections
          .get(candidate)
          .map(a => [a, connect.realConnections.get(a).length])
      );
      neighborCounts.delete(from);
      let end = null;
      let next = null;
      neighborCounts.forEach((val, key) => {
        if (val == 2) {
          end = key;
        } else if (val == 3) {
          next = key;
        }
      });
      if (end) {
        edge.push(end);
        break;
      }
      from = candidate;
      candidate = next;
    }
    return edge;
  }
  return { topEdge, leftEdge };
}


function intersect(a, b) {
  return a.filter(item => b.includes(item));
}

function genGrid(connect, edges)
{
  function findNextNode(node, lastEdge, i) {
    let candidates1 = connect.realConnections.get(node);
    let candidates2 = connect.realConnections.get(lastEdge[i + 1]);
    let intersection = intersect(candidates1, candidates2);
    intersection = intersection.filter(a => a != lastEdge[i]);
    return intersection[0];
  }
  function findNextEdge(start, lastEdge) {
    let from = start;
    let edge = [];
    for (let i = 0; i < lastEdge.length - 1; i++) {
      edge.push(from);
      let next = findNextNode(from, lastEdge, i);
      from = next;
    }
    edge.push(from);
    return edge;
  }
  let grid = [edges.topEdge];
  let prevEdge = edges.topEdge;
  for (let i = 1; i < edges.leftEdge.length; i++) {
    let newEdge = findNextEdge(edges.leftEdge[i], prevEdge);
    grid.push(newEdge);
    prevEdge = newEdge;
  }
  return { grid };
}


function getStartArrangement(start, right, bottom) {
  for (let i = 0; i < 8; i++) {
    let eRotation = start.matchRight(right, i);
    let sRotation = start.matchBottom(bottom, i);
    if (eRotation != -1 && sRotation != -1) {
      return { startRotation: i, eRotation, sRotation };
    }
  }
  return false;
}

function getNextCellRotations(input, id, rotation, rightId, bottomId) {
  let eRotation = input.get(id).matchRight(input.get(rightId), rotation);
  let sRotation = input.get(id).matchBottom(input.get(bottomId), rotation);
  if (eRotation != -1 && sRotation != -1) {
    return { eRotation, sRotation };
  }
  return false;
}

function getSouthCell(input, id, rotation, southId) {
  let sRotation = input.get(id).matchBottom(input.get(southId), rotation);
  if (sRotation != -1) {
    return { sRotation };
  }
  return false;
}

function genFinalGrid(input, connections)
{
  let edges = genEdges(connections);
  let grid = genGrid(connections, edges);
  let { startRotation, eRotation, sRotation } = getStartArrangement(
    input.get(edges.topEdge[0]),
    input.get(edges.topEdge[1]),
    input.get(edges.leftEdge[1])
  );
  let key = (a, b) => a + ',' + b;
  let rotationGrid = new Map([
    [key(0, 0), startRotation],
    [key(1, 0), eRotation],
    [key(0, 1), sRotation]
  ]);
  for (let x = 0; x < grid.grid.length - 1; x++) {
    for (let y = 0; y < grid.grid.length - 1; y++) {
      let ncr = getNextCellRotations(
        input,
        grid.grid[y][x],
        rotationGrid.get(key(x, y)),
        grid.grid[y][x + 1],
        grid.grid[y + 1][x]
      );
      rotationGrid.set(key(x + 1, y), ncr.eRotation);
      rotationGrid.set(key(x, y + 1), ncr.sRotation);
    }
  }
  let x = grid.grid.length - 1;
  let y = grid.grid.length - 2;
  let ncr = getSouthCell(
    input,
    grid.grid[y][x],
    rotationGrid.get(key(x, y)),
    grid.grid[y + 1][x]
  );
  rotationGrid.set(key(x, y + 1), ncr.sRotation);

  let allStrings = [];
  for (let y = 0; y < grid.grid.length; y++) {
    let row = [];
    for (let x = 0; x < grid.grid.length; x++) {
      row.push(input.get(grid.grid[y][x]).str(rotationGrid.get(key(x, y))));
    }
    allStrings.push(row);
  }

  let allTrimmedCells = [];
  for (let y = 0; y < grid.grid.length; y++) {
    let row = [];
    for (let x = 0; x < grid.grid.length; x++) {
      row.push(input.get(grid.grid[y][x]).trim(rotationGrid.get(key(x, y))));
    }
    allTrimmedCells.push(row);
  }

  let allTrimmedStrings = allTrimmedCells.map(a =>
    a.map(b => b.map(c => c.join('')))
  );
  let allFinalStrings = [];
  for (let row = 0; row < allTrimmedStrings.length; row++) {
    for (let i = 0; i < allTrimmedStrings[row][0].length; i++) {
      let rowElements = [];
      for (let col = 0; col < grid.grid.length; col++) {
        rowElements.push(allTrimmedStrings[row][col][i]);
      }
      allFinalStrings.push(rowElements.join(''));
    }
  }
  return allFinalStrings;
}


function _ANSWER_2(input) {
  let cm = connectionMatrix(input);
  let connections = connect(cm);
  let finalGrid = genFinalGrid(input, connections);
  let numHashes = finalGrid.join('').match(/#/g).length;
  return numHashes - 21 * monsterOffsets().length
}


function monsterLiteral(){
  return`                  # 
#    ##    ##    ###
 #  #  #  #  #  # `;
}

function monsterOffsets()
{
  let offsetMatrix = monsterLiteral().split('\n').map(line =>
    line
      .split('')
      .map((char, i) => (char == '#' ? i : -1))
      .filter(a => a != -1)
  );
  let entries = [];
  for (let [i, row] of offsetMatrix.entries()) {
    for (let cell of row) {
      entries.push([i, cell]);
    }
  }
  return entries;
}



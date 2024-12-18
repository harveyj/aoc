module.exports = { _input, _ANSWER_1, _ANSWER_2 };

function _1(md) {
  return md`
# Advent 2020 Day 17!
  `;
}

function _input(input) {
  return input;
}

function processInput(input) {
  let rawCells = input.split("\n").map((a) => a.split(""));
  let minX = -1;
  let minY = -1;
  let minZ = -1;
  let minW = -1;
  let maxX = rawCells.length + 1;
  let maxY = rawCells.length + 1;
  let maxZ = rawCells.length + 1;
  let maxW = rawCells.length + 1;
  let cells = new Map();
  for (let x = 0; x < rawCells.length; x++) {
    for (let y = 0; y < rawCells.length; y++) {
      if (rawCells[y][x] == "#") {
        cells.set(idx(x, y, 0, 0), true);
      }
    }
  }
  return { minX, minY, minZ, minW, maxX, maxY, maxZ, maxW, cells };
}

function processInput3d(input) {
  let rawCells = input.split("\n").map((a) => a.split(""));
  let minX = -1;
  let minY = -1;
  let minZ = -1;
  let maxX = rawCells.length + 1;
  let maxY = rawCells.length + 1;
  let maxZ = rawCells.length + 1;
  let cells = new Map();
  for (let x = 0; x < rawCells.length; x++) {
    for (let y = 0; y < rawCells.length; y++) {
      if (rawCells[y][x] == "#") {
        cells.set(idx3d(x, y, 0), true);
      }
    }
  }
  return { minX, minY, minZ, maxX, maxY, maxZ, cells };
}

function idx(x, y, z, w) {
  return `${x},${y},${z},${w}`;
}

function idx3d(x, y, z) {
  return `${x},${y},${z}`;
}

// TODO clean up all the copypasta
function _ANSWER_1(input) {
  function nextGrid(grid) {
    let cells = new Map();
    for (let x = grid.minX; x < grid.maxX + 1; x++) {
      for (let y = grid.minY; y < grid.maxY + 1; y++) {
        for (let z = grid.minZ; z < grid.maxZ + 1; z++) {
          let count = countNeighbors3d({ x, y, z }, (a) =>
            grid.cells.has(idx3d(a.x, a.y, a.z))
          );
          if (grid.cells.get(idx3d(x, y, z))) {
            if (count == 2 || count == 3) {
              cells.set(idx3d(x, y, z), true);
            }
          } else {
            if (count == 3) {
              cells.set(idx3d(x, y, z), true);
            }
          }
        }
      }
    }
    return {
      minX: grid.minX - 1,
      minY: grid.minY - 1,
      minZ: grid.minZ - 1,
      maxX: grid.maxX + 1,
      maxY: grid.maxY + 1,
      maxZ: grid.maxZ + 1,
      cells,
    };
  }
  let grid = processInput3d(input);
  for (let i = 0; i < 6; i++) {
    grid = nextGrid(grid);
  }
  let i = 0;
  for (const [key, value] of grid.cells) {
    i++;
  }
  return i;
}

function _ANSWER_2(input) {
  function nextGrid(grid) {
    let cells = new Map();
    for (let x = grid.minX; x < grid.maxX + 1; x++) {
      for (let y = grid.minY; y < grid.maxY + 1; y++) {
        for (let z = grid.minZ; z < grid.maxZ + 1; z++) {
          for (let w = grid.minW; w < grid.maxW + 1; w++) {
            let count = countNeighbors({ x, y, z, w }, (a) =>
              grid.cells.has(idx(a.x, a.y, a.z, a.w))
            );
            if (grid.cells.get(idx(x, y, z, w))) {
              if (count == 2 || count == 3) {
                cells.set(idx(x, y, z, w), true);
              }
            } else {
              if (count == 3) {
                cells.set(idx(x, y, z, w), true);
              }
            }
          }
        }
      }
    }
    return {
      minX: grid.minX - 1,
      minY: grid.minY - 1,
      minZ: grid.minZ - 1,
      minW: grid.minW - 1,
      maxX: grid.maxX + 1,
      maxY: grid.maxY + 1,
      maxZ: grid.maxZ + 1,
      maxW: grid.maxW + 1,
      cells,
    };
  }
  let grid = processInput(input);
  for (let i = 0; i < 6; i++) {
    grid = nextGrid(grid);
  }
  let i = 0;
  for (const [key, value] of grid.cells) {
    i++;
  }
  return i;
}

function neighbors3d(obj) {
  let neighbors = [];
  for (let dx of [-1, 0, 1]) {
    for (let dy of [-1, 0, 1]) {
      for (let dz of [-1, 0, 1]) {
        if (!dx && !dy && !dz) {
          continue;
        }
        neighbors.push({
          x: obj.x + dx,
          y: obj.y + dy,
          z: obj.z + dz,
        });
      }
    }
  }
  return neighbors;
}

function neighbors(obj) {
  let neighbors = [];
  for (let dx of [-1, 0, 1]) {
    for (let dy of [-1, 0, 1]) {
      for (let dz of [-1, 0, 1]) {
        for (let dw of [-1, 0, 1]) {
          if (!dx && !dy && !dz && !dw) {
            continue;
          }
          neighbors.push({
            x: obj.x + dx,
            y: obj.y + dy,
            z: obj.z + dz,
            w: obj.w + dw,
          });
        }
      }
    }
  }
  return neighbors;
}

function countNeighbors3d(obj, pred) {
  return neighbors3d(obj)
    .map(pred)
    .reduce((a, b) => a + b, 0);
}

function countNeighbors(obj, pred) {
  return neighbors(obj)
    .map(pred)
    .reduce((a, b) => a + b, 0);
}

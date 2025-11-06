module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 24 - Christmas Eve!`
)}

function _input(input) {
  return processInput(input);
}

function processInput(input) {
  let paths = input
    .split('\n')
    .map(processPath)
  let locs = paths.map(pathToLoc);
  return { paths, locs };
}

function processPath(rawPath) {
  let items = [];
  for (let i = 0; i < rawPath.length; i) {
    if (rawPath[i] == 'n') {
      if (rawPath[i + 1] == 'e') {
        items.push('ne');
      } else if (rawPath[i + 1] == 'w') {
        items.push('nw');
      }
      i += 2;
    } else if (rawPath[i] == 's') {
      if (rawPath[i + 1] == 'e') {
        items.push('se');
      } else if (rawPath[i + 1] == 'w') {
        items.push('sw');
      }
      i += 2;
    } else if (rawPath[i] == 'e') {
      items.push('e');
      i += 1;
    } else if (rawPath[i] == 'w') {
      items.push('w');
      i += 1;
    } else {
      throw new Error('malformed input');
    }
  }
  return items;
}

function pathToLoc(path) {
  let x = 0;
  let y = 0;
  for (let step of path) {
    if (step == 'ne') {
      y -= 1;
      x += 0.5;
    } else if (step == 'nw') {
      y -= 1;
      x -= 0.5;
    } else if (step == 'e') {
      x += 1;
    } else if (step == 'w') {
      x -= 1;
    } else if (step == 'se') {
      y += 1;
      x += 0.5;
    } else if (step == 'sw') {
      y += 1;
      x -= 0.5;
    } else {
      throw new Error('malformed input');
    }
  }
  return { x, y };
}

function GEN_ANSWER_1(input)
{
  let tiles = new Map();
  for (let loc of input.locs) {
    if (tiles.has(loc.x + ' ' + loc.y)) {
      tiles.get(loc.x + ' ' + loc.y).black = !tiles.get(loc.x + ' ' + loc.y)
        .black;
    } else {
      tiles.set(loc.x + ' ' + loc.y, { loc, black: true });
    }
  }
  return Array.from(tiles.values()).filter(a => a.black);
}

function _ANSWER_1(input) {
  return GEN_ANSWER_1(input).length;
}


function k(loc) {
  return loc.x + " " + loc.y
}

function hexNeighbors(loc) {
  return [
    { x: loc.x - 1, y: loc.y },
    { x: loc.x + 1, y: loc.y },
    { x: loc.x - 0.5, y: loc.y + 1 },
    { x: loc.x - 0.5, y: loc.y - 1 },
    { x: loc.x + 0.5, y: loc.y + 1 },
    { x: loc.x + 0.5, y: loc.y - 1 }
  ];
}

function _ANSWER_2(input)
{
  ANSWER_1 = GEN_ANSWER_1(input)
  let locMap = new Map();
  ANSWER_1.forEach(a => {
    if (a.black) {
      locMap.set(k(a.loc), a);
    }
  });
  let newLocMap;
  for (let day = 0; day < 100; day++) {
    newLocMap = new Map();
    let blackLocObjects = locMap.values();
    let candidateLocs = new Array();
    for (let blackLoc of blackLocObjects) {
      candidateLocs = candidateLocs.concat(hexNeighbors(blackLoc.loc));
    }
    for (let candidateLoc of candidateLocs) {
      let neighborsBlack = hexNeighbors(candidateLoc).filter(
        a => locMap.get(k(a)) && locMap.get(k(a)).black
      ).length;
      let thisTile = locMap.get(k(candidateLoc));
      if (thisTile && thisTile.black) {
        if (neighborsBlack == 1 || neighborsBlack == 2) {
          newLocMap.set(k(candidateLoc), { loc: candidateLoc, black: true });
        }
      } else if (neighborsBlack == 2) {
        newLocMap.set(k(candidateLoc), { loc: candidateLoc, black: true });
      }
    }
    // console.log("num tiles", day + 1, newLocMap.size);
    locMap = newLocMap;
  }
  return newLocMap.size;
  /*
  locMap = blah
  newLocMap = {}
  for day
    blackLocs = locMap.map(is it black)
    candidateLocs = ... everything adjacent to blackLocs
    for c in candidateLocs:
      look up all 6 neighbors in locMap, count black
      if black and 0 or > 2
         tile is white
      if white and 2
         tile is black
    print num black tiles in newlocmap
    locmap = newlocmap
    */
}



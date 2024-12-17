module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2021 Day 8!`
)}






function _input(inputRaw,selectedInput,processInput){return(
inputRaw[selectedInput].split("\n").map(processInput)
)}

function _processInput(){return(
function (inLine) {
  let vals = inLine.split("|");
  let tests = vals[0].trim().split(" ");
  let value = vals[1].trim().split(" ");
  return { tests, value };
}
)}

function _ANSWER_1(input)
{
  // 1 - 2 digits
  // 4 - 4 digits
  // 7 - 3 digits
  // 8 - 7 digits
  let total = 0;
  for (let line of input) {
    let value = line.value;
    for (let entry of value) {
      if (
        entry.length == 2 ||
        entry.length == 3 ||
        entry.length == 4 ||
        entry.length == 7
      ) {
        total++;
      }
    }
  }
  return total;
}


function _ANSWER_2_ALT(input)
{
  // 0 has 6 segments, with cc and ff
  // 1 has *2 segments, with cc and ff
  // 2 has 5 segments, only cc
  // 3 has 5 segments, both cc and ff
  // 4 has *4 segments
  // 5 has 5 segments, only ff
  // 6 has 6 segments only ff
  // 7 has *3 segments, aa, cc, ff --> determine aa
  // 8 has *7 segments
  // 9 has 6 segments with cc, ff
  // ALTERNATELY, cc and ff are what 4 (4 segment) and 7 (3 segment) share

  // distinguish 0, 9
  let known = { aa: "", bb: "", cc: "", dd: "", ee: "", ff: "", gg: "" };
  let knownNumbers = ["", "", "", "", "", "", "", "", "", ""];
  let ccff = "";
  let values = [];
  for (let line of input) {
    console.log(line);
    for (let test of line.tests) {
      if (test.length == 2) {
        ccff = test;
        knownNumbers[1] = test;
      } else if (test.length == 4) {
        knownNumbers[4] = test;
      } else if (test.length == 3) {
        knownNumbers[7] = test;
      } else if (test.length == 7) {
        knownNumbers[8] = test;
      }
    }
    for (let test of line.tests) {
      if (test.length == 6) {
        for (let c of ccff) {
          if (!test.includes(c)) {
            console.log("c found:", c);
            console.log("f found:", ccff.replace(c, ""));
            known.cc = c;
            known.ff = ccff.replace(c, "");
            knownNumbers[6] = test;
          }
        }
      }
    }
    for (let test of line.tests) {
      if (test.length == 5) {
        if (!test.includes(known.ff)) {
          knownNumbers[2] = test;
        } else if (!test.includes(known.cc)) {
          knownNumbers[5] = test;
        } else {
          knownNumbers[3] = test;
        }
      }
    }
    for (let test of line.tests) {
      if (test.length == 6 && test != knownNumbers[6]) {
        let allFound = true;
        for (let c of knownNumbers[3]) {
          if (!test.includes(c)) {
            allFound = false;
          }
        }
        if (allFound) {
          knownNumbers[9] = test;
        } else {
          knownNumbers[0] = test;
        }
      }
    }
    for (let i = 0; i < knownNumbers.length; i++) {
      knownNumbers[i] = knownNumbers[i].split("").sort().join("");
    }
    console.log(knownNumbers);
    let num = "";
    for (let numSegments of line.value) {
      num += knownNumbers.indexOf(numSegments.split("").sort().join(""));
    }
    values.push(num * 1);
  }
  return values.reduce((a, b) => a + b);
}


function _allPermutations(){return(
function (inVect) {
  function allPermutationsHelper(inVect) {
    if (inVect.length == 1) {
      return inVect;
    }
    let ret = [];
    for (let i = 0; i < inVect.length; i++) {
      let val = inVect[i];
      let newVect = inVect.filter((a) => a != val);
      let desc = allPermutationsHelper(newVect);
      ret.push([val, desc]);
    }
    return [""].concat(ret);
  }
  function allPaths(prefix, tree) {
    if (tree.length == 1) {
      return [prefix + tree[0]];
    }
    let ret = [];
    for (let i = 1; i < tree.length; i++) {
      let accumulated = allPaths(prefix + tree[0], tree[i]);
      ret = ret.concat(accumulated);
    }
    return ret;
  }
  let tree = allPermutationsHelper(inVect);
  return allPaths("", tree);
  return tree;
}
)}

function _9(allPermutations){return(
allPermutations(["a", "b", "c", "d", "e", "f", "g"])
)}

function _translate(){return(
function (inStr, key) {
  let ret = [];
  for (let c of inStr) {
    let num = c.charCodeAt(0);
    ret.push(key[num - 97]);
  }
  return ret.sort().join("");
}
)}

function _11(translate){return(
translate("aaaba", "dcab")
)}

function _12(){return(
"dbca".split("").sort().join("")
)}


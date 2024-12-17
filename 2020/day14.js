module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 14!`
)}



function _input(inputRaw,selectedInput,processInstr){return(
inputRaw[selectedInput].split('\n').map(processInstr)
)}

function _processInstr(){return(
function(instr) {
  let maskRe = /mask = (.*)/;
  let memRe = /mem\[(\d+)\] = (\d+)/;
  let maskMatch = instr.match(maskRe);
  let memMatch = instr.match(memRe);
  function processMask(mask) {
    let ors = [];
    let ands = [];
    for (let i = 0; i < 36; i++) {
      let val = 2 ** (35 - i);
      if (mask.substring(i, i + 1) == '1') {
        ors.push(val);
      } else if (mask.substring(i, i + 1) == '0') {
        ands.push(2 ** 36 - 1 - val);
      }
    }
    return { ors, ands, mask};
  }
  if (maskMatch) {
    return { op: 'mask', rval: processMask(maskMatch[1]) };
  } else if (memMatch) {
    return {
      op: 'mem',
      lval: memMatch[1] * 1,
      rval: memMatch[2] * 1
    };
  }
  return { op: "ERROR" };
}
)}

function _ANSWER_1(or,and,input)
{
  let mem = new Map();
  let mask = null;
  function applyMask(val) {
    for (let orVal of mask.ors) {
      val = or(val, orVal);
    }
    for (let andVal of mask.ands) {
      val = and(val, andVal);
    }
    console.log(val);
    return val;
  }
  for (let inst of input) {
    if (inst.op == "mask") {
      mask = inst.rval;
    } else if (inst.op == "mem") {
      mem.set(inst.lval, applyMask(inst.rval));
    }
  }
  let total = 0;
  for (let val of mem.values()) {
    total += val;
  }
  return total;
}


function _setCharAt(){return(
function setCharAt(str, index, chr) {
  if (index > str.length - 1) return str;
  return str.substring(0, index) + chr + str.substring(index + 1);
}
)}

function _ANSWER_2(or,and,setCharAt,input)
{
  function applyMask(mask, val) {
    for (let i = 0; i < 36; i++) {
      let bit = 2 ** (35 - i);
      if (mask.substring(i, i + 1) == 'a') {
        val = or(val, bit);
      }
      if (mask.substring(i, i + 1) == 'c') {
        val = and(val, 2 ** 36 - 1 - bit);
      }
    }
    return val;
  }
  function enumerateAddrs(mask) {
    for (let i = 0; i < 36; i++) {
      if (mask[i] == 'X') {
        let maskOne = setCharAt(mask, i, 'a');
        let maskZero = setCharAt(mask, i, 'c');
        let masksOne = enumerateAddrs(maskOne);
        let masksZero = enumerateAddrs(maskZero);
        return masksZero.concat(masksOne);
      } else if (mask[i] == '0') {
        mask = setCharAt(mask, i, 'b');
      } else if (mask[i] == '1') {
        mask = setCharAt(mask, i, 'a');
      }
    }
    return [mask];
  }

  let mem = new Map();
  let masks = null;
  let appliedMasks = [];
  for (let inst of input) {
    if (inst.op == "mask") {
      masks = enumerateAddrs(inst.rval.mask);
    } else if (inst.op == "mem") {
      for (let mask of masks) {
        mem.set(applyMask(mask, inst.lval), inst.rval);
        appliedMasks.push(mask, inst.lval, applyMask(mask, inst.lval));
      }
    }
  }
  let total = 0;
  for (let val of mem.values()) {
    total += val;
  }
  return total;
}





function _and(){return(
function and(v1, v2) {
    var hi = 0x80000000;
    var low = 0x7fffffff;
    var hi1 = ~~(v1 / hi);
    var hi2 = ~~(v2 / hi);
    var low1 = v1 & low;
    var low2 = v2 & low;
    var h = hi1 & hi2;
    var l = low1 & low2;
    return h*hi + l;
}
)}

function _or(){return(
function or(v1, v2) {
  var hi = 0x80000000;
  var low = 0x7fffffff;
  var hi1 = ~~(v1 / hi);
  var hi2 = ~~(v2 / hi);
  var low1 = v1 & low;
  var low2 = v2 & low;
  var h = hi1 | hi2;
  var l = low1 | low2;
  return h * hi + l;
}
)}


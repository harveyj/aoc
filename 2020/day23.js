import Denque from 'denque';

function _1(md){return(
md`# Advent 2020 Day 23!`
)}

export function _input(input) {
  return processInput(input)
}

function processInput(input) {
  return input.split('').map(a => a * 1);
}

function rotate(dq, n){
  if (n > 0) {
   // +1 moves right
    for (let i = 0; i < n; i++){
      dq.push(dq.shift());
    }
  } else {
    // -1 moves left
    for (let i = 0; i < -n; i++){
     dq.unshift(dq.pop());
    }
  }
}

export function _ANSWER_1(input, two)
{
  const dq = new Denque(input);
  let MAX = 9;
  let MAX_ITERS = 100;
  if (two) {
    MAX=999999
    MAX_ITERS=10000000
  }
  for (let i = 10; i < MAX+1; i++) {
    dq.push(i)
  }
  // console.log('dq', dq.toArray().toString())
  for (let i = 0; i < MAX_ITERS; i++) {
    let vals = [];
    if (i % 100 == 0) {
      console.log(i)
    }
    // current cup is always front of array
    let destVal = dq.peekFront() - 1;
    if (destVal <= 0) {
      destVal += MAX;
    }
    rotate(dq, 1)
    vals.push(dq.shift());
    vals.push(dq.shift());
    vals.push(dq.shift());
    // console.log('pick up', vals)
    while (vals.indexOf(destVal) != -1) {
      destVal--;
      if (destVal <= 0) {
        destVal += MAX;
      }
    }
    // console.log({destVal})

    let tgtNextVal = dq.peekFront();
    let scans = 0;
    while (dq.peekFront() != destVal) {
      rotate(dq, -1)
      scans += 1
      if (scans > 50000) {
        console.log('50k', i)
        scans -= 10000000000
      }
      // console.log('scanning', dq.toArray(), vals, destVal)
    }
    // console.log(dq)
    // go one past target
    rotate(dq, 1)

    dq.unshift(vals.pop())
    dq.unshift(vals.pop())
    dq.unshift(vals.pop())
    while (dq.peekFront() != tgtNextVal) {
      rotate(dq, 1);
    }
    // console.log('final,', dq.toArray().toString())
    // const printer = new Deque(dq);
    // printer.rotate(i+1)
    // console.log('final,', ,', dq.toArray().toString())

    // console.log('****')
  }
  while (dq.peekFront() != 1) {
    rotate(dq, -1)
  }
  dq.shift()
      return dq.toArray().join('');
}

export function _ANSWER_2(input)
{
  return _ANSWER_1(input, true)
}

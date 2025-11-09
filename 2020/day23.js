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

export function _ANSWER_1(input, two)
{
  // key = id (int); val = prev (int), next (int)
  const nextPrevMap = {};
  let CUPS = 9;
  let MAX_ITERS = 100;
  if (two) {
    CUPS = 1000000
    MAX_ITERS = 10000000
  }
  let lastValue = (CUPS == input.length) ? input[input.length-1] : CUPS;
  let firstValue = input[0];
  let prevValue = lastValue;
  nextPrevMap[prevValue] = {}
  for (let i = 0; i < CUPS; i++) {
      let value = (i < input.length)? input[i] : i+1;
      nextPrevMap[value] = {}
      nextPrevMap[value].prev = prevValue
      nextPrevMap[prevValue].next = value;
      prevValue = value;
  }
  // console.log({firstValue, lastValue})
  nextPrevMap[lastValue].next = firstValue;
  nextPrevMap[firstValue].prev = lastValue;
  // console.log(nextPrevMap)

  let currentCup = input[0];
  
  for (let i = 0; i < MAX_ITERS; i++) {
    // The crab picks up the three cups that are immediately clockwise of the current cup. They are
    // removed from the circle; cup spacing is adjusted as necessary to maintain the circle. 
    let firstPickup = nextPrevMap[currentCup].next;
    let secondPickup = nextPrevMap[firstPickup].next;
    let thirdPickup = nextPrevMap[secondPickup].next;
    let ringRejoin = nextPrevMap[thirdPickup].next;
    nextPrevMap[currentCup].next = ringRejoin;
    nextPrevMap[ringRejoin].prev = currentCup;
    // The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If
    // this would select one of the cups that was just picked up, the crab will keep subtracting one
    // until it finds a cup that wasn't just picked up. If at any point in this process the value goes
    // below the lowest value on any cup's label, it wraps around to the highest value on any cup's
    // label instead. 
    let pickupIds = [firstPickup, secondPickup, thirdPickup];
    let destinationCup = currentCup-1;
    if (destinationCup == 0){
        destinationCup += CUPS
    }

    while (pickupIds.includes(destinationCup)) {
      destinationCup--;
      if (destinationCup == 0){
        destinationCup += CUPS
      }
    }
    if (destinationCup == 0){
      destinationCup = CUPS
    }

    // The crab places the cups it just picked up so that they are immediately clockwise
    // of the destination cup. They keep the same order as when they were picked up. 
    // console.log(nextPrevMap)
  // console.log(destinationCup)
    let destPlusOne = nextPrevMap[destinationCup].next;
    nextPrevMap[destinationCup].next = firstPickup;
    nextPrevMap[firstPickup].prev = destinationCup;
    
    nextPrevMap[destPlusOne].prev = thirdPickup;
    nextPrevMap[thirdPickup].next = destPlusOne;
    
    // The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    currentCup = nextPrevMap[currentCup].next;
    // console.log(nextPrevMap);
    // console.log(currentCup, log(nextPrevMap, currentCup))
    // console.log('********')
  } 
  if (two) {
    return nextPrevMap[1].next * nextPrevMap[nextPrevMap[1].next].next;
  } else {
    return log(nextPrevMap, 1)
  }
}

function log(nextPrevMap, startCup) {
  let ret = '';
  let currentCup = nextPrevMap[startCup].next
  while (currentCup != startCup) {
    ret += currentCup
    currentCup = nextPrevMap[currentCup].next;
  }
  return ret;
}

export function _ANSWER_2(input)
{
  // return
  return _ANSWER_1(input, true)
}

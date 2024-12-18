module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 23!`
)}

function _input(input) {
  return processInput(input)
}

function processInput(input) {
  return input.split('').map(a => a * 1);
}

function _ANSWER_1(input)
{
  let deck = [...input];
  let deckIdx = 0;
  for (let i = 0; i < 100; i++) {
    let currentCup = deck[deckIdx];

    let pickup = deck.splice(deckIdx + 1, 3);
    // account for splice not wrapping
    if (pickup.length < 3) {
      pickup = pickup.concat(deck.splice(0, 3 - pickup.length));
    }
    let destination = currentCup;
    do {
      destination -= 1;
      if (destination == 0) {
        destination = 9;
      }
    } while (pickup.indexOf(destination) != -1 && destination != currentCup);
    let destinationIdx = deck.indexOf(destination);
    deck.splice(destinationIdx + 1, 0, ...pickup);
    deckIdx = (deck.indexOf(currentCup) + 1) % deck.length;
  }

  let ret = [];
  deckIdx = deck.indexOf(1);
  for (let i = 0; i < deck.length; i++) {
    let idx = (deckIdx + i) % deck.length;
    ret.push(deck[idx]);
  }
  return ret.slice(1).join('');
}

// TODO lol crashes the vm
function _ANSWER_2(input)
{
  return 0;
  let MAX = 100;
  let filler = [...Array(MAX - input.length)];
  filler = filler.map((a, idx) => idx + input.length + 1);
  let deck = input.concat(filler);
  let deckIdx = 0;
  let answerMap = new Map();
  for (let i = 0; i < 10000000; i++) {
    let currentCup = deck[deckIdx];

    let pickup = deck.splice(deckIdx + 1, 3);
    // account for splice not wrapping
    if (pickup.length < 3) {
      pickup = pickup.concat(deck.splice(0, 3 - pickup.length));
    }
    let destination = currentCup;
    do {
      destination -= 1;
      if (destination == 0) {
        destination = MAX - 1;
      }
    } while (pickup.indexOf(destination) != -1 && destination != currentCup);
    let destinationIdx = deck.indexOf(destination);
    deck.splice(destinationIdx + 1, 0, ...pickup);
    deckIdx = (deck.indexOf(currentCup) + 1) % deck.length;

    if (answerMap.has('' + deck)) {
      answerMap.get('' + deck).push(i);
    } else {
      answerMap.set('' + deck, [i]);
    }
  }

  // return deck[deck.indexOf(1) + 1] * deck[deck.indexOf(1) + 2];
  // console.log(answerMap)
  return Array.from(answerMap.entries()).filter((a, b) => a[1].length > 1);
}



module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 22!`
)}



function _input(input){
  return processInput(input);
}

function processInput(input) {
  function processDeck(rawDeck) {
    let deck = rawDeck
      .split('\n')
      .filter(a => a)
      .map(a => a * 1);

    return deck;
  }
  return input
    .split('Player 1:')[1]
    .split('Player 2:')
    .map(processDeck);
}

function _ANSWER_1(input){
  function play(player1, player2) {
    player1 = [...player1];
    player2 = [...player2];
    while (true) {
      let top1 = player1.shift();
      let top2 = player2.shift();
      let player1Won = top1 > top2;
      if (player1Won) {
        player1.push(top1);
        player1.push(top2);
      } else {
        player2.push(top2);
        player2.push(top1);
      }
      if (player1.length == 0) {
        return { player1Won: false, deck: player2 };
      } else if (player2.length == 0) {
        return { player1Won: true, deck: player1 };
      }
    }
  }
  let ret = play(input[0], input[1]);
  let size = ret.deck.length;
  return ret.deck.map((val, i) => val * (size - i)).reduce((a, b) => a + b, 0);
}


function _ANSWER_2(input)
{
  function play(player1, player2) {
    player1 = [...player1];
    player2 = [...player2];
    let seenStates = new Set();
    while (true) {
      let state = player1.toString() + player2.toString();
      if (seenStates.has(state)) {
        // 'terminating the countryside'
        return { player1Won: true, deck: player1 };
      }
      seenStates.add(state);
      let top1 = player1.shift();
      let top2 = player2.shift();
      let player1Won = top1 > top2;
      if (top1 < player1.length + 1 && top2 < player2.length + 1) {
        // recurse!
        player1Won = play(player1.slice(0, top1), player2.slice(0, top2))
          .player1Won;
      }
      if (player1Won) {
        player1.push(top1);
        player1.push(top2);
      } else {
        player2.push(top2);
        player2.push(top1);
      }
      if (player1.length == 0) {
        return { player1Won: false, deck: player2 };
      } else if (player2.length == 0) {
        return { player1Won: true, deck: player1 };
      }
    }
  }
  let ret = play(input[0], input[1]);
  let size = ret.deck.length;
  return ret.deck.map((val, i) => val * (size - i)).reduce((a, b) => a + b, 0);
}



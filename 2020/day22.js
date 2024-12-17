module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 22!`
)}



function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(){return(
function(input) {
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
)}

function _selectedInput(html,inputRaw)
{
  return html`
    <select>
      ${Object.keys(inputRaw).map(
        key => `<option value=${key}>${key}</option>`
      )}
    </select>
 `;
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
        console.log('terminating the countryside');
        return { player1Won: true, deck: player1 };
      }
      console.log(seenStates.size);
      seenStates.add(state);
      // console.log(player1);
      // console.log(player2);
      let top1 = player1.shift();
      let top2 = player2.shift();
      let player1Won = top1 > top2;
      if (top1 < player1.length + 1 && top2 < player2.length + 1) {
        console.log("recurse!");
        player1Won = play(player1.slice(0, top1), player2.slice(0, top2))
          .player1Won;
      }
      if (player1Won) {
        player1.push(top1);
        player1.push(top2);
        // console.log("player 1 wins!\n");
      } else {
        player2.push(top2);
        player2.push(top1);
        // console.log("player 2 wins!\n");
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



#!/usr/local/bin/node
const fs = require('node:fs');


fs.readFile('./2020/inputs/answers.txt', 'utf8', (err, data) => {
  check(data);
});

function check(raw_answers) {
  let answers = raw_answers.split('\n');
  answers = answers.map(row => row.split(' ').map(a=>eval(a)));
  for (let i = 1; i < 26; i++) {
    const day = require(`./day${i}.js`);
    fs.readFile(`./2020/inputs/${i}.txt`, 'utf8', (err, data) => {
      let [dayId, correct1, correct2] = answers[i-1];
      let input = day._input(data.trim());
      let answer1 = day._ANSWER_1(input);
      let answer2 = day._ANSWER_2(input);
      if (answer1 == correct1) {
        console.log(`${i} CORRECT pt1 ${answer1}`)
      } else {
        console.log(`${i} INCORRECT pt1 ${answer1}, ${correct1}`);
      }
      if (answer2 == correct2) {
        console.log(`${i} CORRECT pt2 ${answer2}`)
      } else {
        console.log(`${i} INCORRECT pt2 ${answer2}, ${correct2}`);
      }
    }); 
  };
}
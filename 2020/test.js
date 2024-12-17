#!/usr/local/bin/node
const fs = require('node:fs');


fs.readFile('./inputs/answers.txt', 'utf8', (err, data) => {
  check(data);
});

function check(answers) {
  console.log(answers)
  for (let i = 1; i < 26; i++) {
    const day = require(`./day${i}.js`);
    fs.readFile(`./inputs/${i}.txt`, 'utf8', (err, data) => {
      let input = day._input(data);
      let answer1 = day._ANSWER_1(input);
      let answer2 = day._ANSWER_2(input);
    }); 
  };
}
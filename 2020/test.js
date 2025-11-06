#!/usr/bin/env node

import fs from 'fs';
import { Command } from 'commander';
const program = new Command();

program
  .name('mycli')
  .description('Example Node.js CLI')
  .version('1.0.0')
  .option('-d, --day <number>', 'day', 0)
  .parse();

const opts = program.opts();
console.log(opts);


fs.readFile('./2020/inputs/answers.txt', 'utf8', (err, data) => {
  check(data);
});

function check(raw_answers) {
  let answers = raw_answers.split('\n');
  answers = answers.map(row => row.split(' ').map(a=>eval(a)));
  let days = [...Array(25)].keys().map(i=>i+1);
  if (opts.day) {
    days = [opts.day];
  }
  (async () => {
  for (const day_id of days) {
    const day = await import(`./day${day_id}.js`);
    fs.readFile(`./2020/inputs/${day_id}.txt`, 'utf8', (err, data) => {
      data=data.split('\n\n\n')[0];
      let [dayId, correct1, correct2] = answers[1*day_id-1];
      let input = day._input(data.trim());
      let answer1 = day._ANSWER_1(input);
      let answer2 = day._ANSWER_2(input);
      if (answer1 == correct1) {
        console.log(`${day_id} CORRECT pt1 ${answer1}`)
      } else {
        console.log(`${day_id} INCORRECT pt1 ${answer1}, ${correct1}`);
      }
      if (answer2 == correct2) {
        console.log(`${day_id} CORRECT pt2 ${answer2}`)
      } else {
        console.log(`${day_id} INCORRECT pt2 ${answer2}, ${correct2}`);
      }
    }); 
  };
})()
}
module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 4!`
)}

function _input(INPUT){return(
INPUT.split('\n\n')
)}

function _ANSWER_1(input)
{
  let total = 0;
  for (let i = 0; i < input.length; i++) {
    let row = input[i];
    if (
      row.match(/ecl:/g) &&
      row.match(/pid:/g) &&
      row.match(/eyr:/g) &&
      row.match(/hcl:/g) &&
      row.match(/byr:/g) &&
      row.match(/iyr:/g) &&
      row.match(/hgt:/g)
    ) {
      total += 1;
    }
  }
  return total;
}

function parseLine(){return(
function(line) {
  let ecl = line.match(/ecl:(\w\w\w)/);
  let pid = line.match(/pid:(\d+)/);
  let eyr = line.match(/eyr:(\d\d\d\d)/);
  let hcl = line.match(/hcl:#([abcdef0123456789]{6})/);
  let byr = line.match(/byr:(\d\d\d\d)/);
  let iyr = line.match(/iyr:(\d\d\d\d)/);
  let hgt = line.match(/hgt:(\d+)(cm|in)/);
  return {
    ecl: ecl && ecl[1],
    pid: pid && pid[1],
    eyr: eyr && eyr[1],
    hcl: hcl && hcl[1],
    byr: byr && byr[1],
    iyr: iyr && iyr[1],
    hgt: hgt && [hgt[1], hgt[2]]
  };
}
)}

function validBirth(){return(
function(match) {
  return match.byr && 1920 <= match.byr * 1 && match.byr * 1 <= 2002;
}
)}

function validIssue(){return(
function(match) {
  return 2010 <= match.iyr * 1 && (match.iyr && match.iyr * 1 <= 2020);
}
)}

function validExpiration(){return(
function(match) {
  return 2020 <= match.eyr * 1 && (match.eyr && match.eyr * 1 <= 2030);
}
)}

function validHeight(){return(
function(match) {
  if (!match || !match.hgt) {
    return false;
  }
  if (match.hgt[1] == 'cm') {
    return 150 <= match.hgt[0] * 1 && match.hgt[0] * 1 <= 193;
  } else if (match.hgt[1] == 'in') {
    return 59 <= match.hgt[0] * 1 && match.hgt[0] * 1 <= 76;
  }
  return false;
}
)}

function validHair(){return(
function(match) {
  return match.hcl && match.hcl != '';
}
)}

function validEye(){return(
function(match) {
  return (
    match.ecl && "amb blu brn gry grn hzl oth".split(' ').includes(match.ecl)
  );
}
)}

function validPassportId(){return(
function(match) {
  return match.pid && match.pid != '' && match.pid.length == 9;
}
)}

function answer2(input,parseLine,validBirth,validIssue,validExpiration,validHeight,validHair,validEye,validPassportId)
{
  let total = 0;
  let valids = [];
  for (let i = 0; i < input.length; i++) {
    let row = input[i];
    let match = parseLine(row);
    let valid = true;
    valid &= validBirth(match);
    valid &= validIssue(match);
    valid &= validExpiration(match);
    valid &= validHeight(match);
    valid &= validHair(match);
    valid &= validEye(match);
    valid &= validPassportId(match);
    if (valid) {
      total += 1;
      valids.push(row);
    }
  }
  return valids;
}

function _ANSWER_2(input) {
  return answer2(input,parseLine,validBirth,validIssue,validExpiration,validHeight,validHair,validEye,validPassportId);
}

function results(validBirth,parseLine,validHeight,validHair,validEye,validPassportId){return(
[
  [validBirth(parseLine('byr:2002'))],
  [validBirth(parseLine('byr:2003'))],
  [validHeight(parseLine('hgt:60in')), validHeight(parseLine('hgt:190cm'))],
  [validHeight(parseLine('hgt:190in')), validHeight(parseLine('hgt:190'))],
  [validHair(parseLine('hcl:#123abc'))],
  [validHair(parseLine('hcl:123abc')), validHair(parseLine('hcl:#123abz'))],
  [validEye(parseLine('ecl:brn'))],
  [validEye(parseLine('ecl:wat'))],
  [validPassportId(parseLine('pid:000000001'))],
  [validPassportId(parseLine('pid:0123456789'))]
]
)}


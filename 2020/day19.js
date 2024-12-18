// https://observablehq.com/@harveyj/advent-2020-day-19@2046
module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 19!`
)}

function _input(input) {
  return processInput(input);
}

function processInput(input) {
  function processField(input) {
    if (input == "\"a\"" || input == "\"b\"") {
      return { op: eval(input) };
    }
    return { op: 'rule', operands: [input * 1] };
  }
  function processClause(clause) {
    console.log(clause);
    let fields = clause
      .split(' ')
      .filter(a => a.trim())
      .map(processField);
    return fields;
  }
  function processRule(input) {
    let [key, vals] = input.split(':');
    key = key * 1;
    let fullOp = null;
    if (input.indexOf('|') != -1) {
      vals = vals.split('|').map(processClause);
      fullOp = {
        op: 'or',
        operands: vals.map(a => ({ op: 'and', operands: a }))
      };
    } else {
      fullOp = { op: 'and', operands: processClause(vals) };
    }
    return [key, fullOp];
  }
  let [rules, messages] = input.split('\n\n');
  rules = rules.split('\n').map(processRule);
  messages = messages.split('\n');
  return { rules: new Map(rules), messages };
}

function _ANSWER_1(input)
{
  let messages = [];
  for (let message of input.messages) {
    let res = applyRule(input, input.rules.get(0), message, 0, new Map());
    if (
      res.ruleApplies &&
      Array.from(res.consumedLengths).indexOf(message.length) != -1
    ) {
      messages.push([message, true, res]);
    } else {
      messages.push([message, false, res]);
    }
  }
  return messages.filter(a => a[1]);
}

function _errors(ANSWER_1,CORRECT)
{
  let wrong = [];
  for (let answer of ANSWER_1) {
    if (CORRECT.indexOf(answer[0]) == -1) {
      wrong.push(answer);
    }
  }
  return wrong;
}

function applyRule(input, rule, message, consumed) {
  if (rule.op == 'a') {
    return message[consumed] == 'a'
      ? { ruleApplies: true, message, consumedLengths: new Set([consumed + 1]) }
      : { ruleApplies: false, message };
  } else if (rule.op == 'b') {
    return message[consumed] == 'b'
      ? { ruleApplies: true, consumedLengths: new Set([consumed + 1]) }
      : { ruleApplies: false };
  } else if (rule.op == 'rule') {
    return applyRule(input.rules.get(rule.operands[0]), message, consumed);
  } else if (rule.op === 'or') {
    let ruleApplies = false;
    let consumedLengths = new Set();
    for (let orBlock of rule.operands) {
      let res = applyRule(orBlock, message, consumed);
      if (res.ruleApplies) {
        consumedLengths = new Set([...consumedLengths, ...res.consumedLengths]);
        ruleApplies = true;
      }
    }
    return { ruleApplies, consumedLengths };
  } else if (rule.op === 'and') {
    let ruleApplies = true;
    let potentialConsumedLengths = new Set([consumed]);
    for (let andClause of rule.operands) {
      let newPotentialConsumedLengths = new Set();
      let someStringWorks = false;
      for (let consumedLength of potentialConsumedLengths) {
        let res = applyRule(andClause, message, consumedLength);
        if (res.ruleApplies) {
          newPotentialConsumedLengths = new Set([
            ...newPotentialConsumedLengths,
            ...res.consumedLengths
          ]);
          someStringWorks = true;
        }
      }
      if (someStringWorks) {
        potentialConsumedLengths = new Set(newPotentialConsumedLengths);
      } else {
        ruleApplies = false;
      }
    }
    return { ruleApplies, consumedLengths: potentialConsumedLengths };
  }
  return []
  throw new Error("fell off the end" + rule);
}

function findLengths(rule) {
  if (rule.op == 'a') {
    return [1];
  } else if (rule.op == 'b') {
    return [1];
  } else if (rule.op === 'or') {
    let possibles = [];
    for (let orBlock of rule.operands) {
      possibles = possibles.concat(findLengths(orBlock));
    }
    return possibles;
  } else if (rule.op === 'and') {
    let possibles = [];
    for (let andClause of rule.operands.map(a => input.rules.get(a))) {
      console.log(andClause);
      possibles = enumerateAll(possibles, findLengths(andClause));
    }
    return possibles;
  }
  // throw new Error("fell off the end" + rule);
  return []
}

function enumerateAll(entries) {
  let possibles = new Set([[]]);
  for (let entry of entries) {
    let newPossibles = new Set();
    for (let possible of possibles) {
      for (let subEntry of entry) {
        newPossibles.add(possible.concat(subEntry));
      }
    }
    possibles = new Set(newPossibles);
  }
  return Array.from(possibles);
}

function _ANSWER_2()
{
}



import assert from 'assert';   // ES modules

function _1(md){return(
md`# Advent 2020 Day 19 take 2!`
)}

export function _input(input){
  return processInput(input)
}

function processInput(input) {
  function processField(input) {
    if (input == "\"a\"" || input == "\"b\"") {
      return { op: 'literal', operands: [eval(input)] };
    }
    return { op: 'rule', operands: [input * 1] };
  }
  function processClause(clause) {
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



export function _ANSWER_1(input)
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
  return messages.filter(a => a[1]).length;
}


export function _ANSWER_2(input) {
  let messages = new Set();
  // 8 is magic # from inspection
  let MAGIC = 8
  for (let a = 0; a < input.messages.length; a++) {
    let message = input.messages[a];
    message.trim()
    let validPrefix = true;
    let applications = 0;
    while (validPrefix && applications * MAGIC < message.length) {
      let res = applyRule(input, input.rules.get(42), message, applications * MAGIC);
      if (res.ruleApplies) {
        applications++;
      } else {
        validPrefix = false;
      }
    }
    if (applications < 2) {
      continue;
    }
    for (let j = 0; j < applications - 1; j++) {
      let res2 = applyRule(input, input.rules.get(31), message, (applications + j) * MAGIC);
      if (res2.ruleApplies) {
        assert(res2.consumedLengths.size == 1);
        if (res2.consumedLengths.has(message.length)){
          messages.add(message) 
          break;
        }
      } else {
        break
      }
    }
  }
  return Array.from(messages).length;
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
  if (rule.op == 'literal') {
    let compareString = message.substring(
      consumed,
      consumed + rule.operands[0].length
    );
    if (compareString === rule.operands[0]) {
      return {
        ruleApplies: true,
        message,
        consumedLengths: new Set([consumed + 1])
      };
    } else {
      return { ruleApplies: false, message };
    }
  } else if (rule.op == 'rule') {
    return applyRule(input, input.rules.get(rule.operands[0]), message, consumed);
  } else if (rule.op === 'or') {
    let ruleApplies = false;
    let consumedLengths = new Set();
    for (let orBlock of rule.operands) {
      let res = applyRule(input, orBlock, message, consumed);
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
        let res = applyRule(input, andClause, message, consumedLength);
        if (res.ruleApplies) {
          newPotentialConsumedLengths = new Set([
            ...newPotentialConsumedLengths,
            ...res.consumedLengths,
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
  throw new Error("fell off the end" + rule);
}
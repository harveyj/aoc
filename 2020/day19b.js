module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 19 take 2!`
)}



function _input(processInput,inputRaw,selectedInput){return(
processInput(inputRaw[selectedInput])
)}

function _processInput(){return(
function(input) {
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
)}




function _ANSWER_1(input,applyRule)
{
  let messages = [];
  for (let message of input.messages) {
    let res = applyRule(input.rules.get(0), message, 0, new Map());
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


function _ANSWER_2(input,applyRule)
{
  let messages = [];
  for (let message of input.messages) {
    let rule42Results = [];
    for (let i = 0; i < 5; i++) {
      let res = applyRule(input.rules.get(42), message, 0);
      return res;
      if (res.ruleApplies) {
        res.consumed;
      }
    }
  }
  return messages;
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


function _CORRECT(){return(
`bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba`.split('\n')
)}

function _applyRule(input){return(
function applyRule(rule, message, consumed) {
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
    let newPotentialConsumedLengths = new Set();
    for (let andClause of rule.operands) {
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
  throw new Error("fell off the end" + rule);
}
)}

function _findLengths(input,enumerateAll){return(
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
  throw new Error("fell off the end" + rule);
}
)}

function _enumerateAll(){return(
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
)}

function _14(enumerateAll){return(
enumerateAll([[1, 3], [2, 4]])
)}


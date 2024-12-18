module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 18!`
)}

function _input(input){
  return input.split('\n')
  .map(a => a)
  .map(processInput)
}

function processInput(input) {
  function processInputHelper(input, start) {
    let out = [];
    let lastNum = null;
    for (let i = start; i < input.length; ) {
      // console.log(out, i, input[i]);
      if (input[i] == '(') {
        let ret = processInputHelper(input, i + 1);
        out.push(ret.out);
        i = ret.end;
      } else if (input[i] == '*') {
        out.push('*');
        i += 1;
      } else if (input[i] == '+') {
        out.push('+');
        i += 1;
      } else if (input[i] * 1) {
        out.push(input[i] * 1);
        i += 1;
      } else if (input[i] == ')') {
        return { out, end: i + 1 };
      } else {
        i += 1;
      }
    }
    return out;
  }
  return processInputHelper(input, 0);
}


function _ANSWER_1(input)
{
  function evaluate(expr) {
    if (typeof expr === "number") {
      return expr;
    }
    let tot = evaluate(expr[0]);
    for (let i = 1; i < expr.length; i += 2) {
      if (expr[i] == '*') {
        tot *= evaluate(expr[i + 1]);
      } else if (expr[i] == '+') {
        tot += evaluate(expr[i + 1]);
      }
    }
    return tot;
  }
  return input.map(evaluate).reduce((a, b) => a + b, 0);
}


function _ANSWER_2(input)
{
  function evaluate(expr) {
    if (typeof expr === "number") {
      return expr;
    }
    let tot = evaluate(expr[0]);
    for (let i = 1; i < expr.length; i += 2) {
      if (expr[i] == '*') {
        tot *= evaluate(expr[i + 1]);
      } else if (expr[i] == '+') {
        tot += evaluate(expr[i + 1]);
      }
    }
    return tot;
  }
  function process(expr) {
    if (typeof expr === "number" || !expr) {
      return expr;
    }
    for (let i = 0; i < expr.length; i++) {
      if (Array.isArray(expr[i])) {
        // console.log(JSON.parse(JSON.stringify(expr[i])));
        process(expr[i]);
      }
      if (expr[i] == '+') {
        let lval = process(expr[i + 1]);
        // console.log(lval);
        expr.splice(i - 1, 3, [expr[i - 1], '+', lval]);
      }
    }
    return expr;
  }
  return input
      .map(process)
      .map(evaluate)
      .reduce((a, b) => a + b, 0);
}



module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _input(INPUT){
  return processInput(INPUT);
}

function processInput(input) {
  let nearby = input
    .split("nearby tickets:\n")[1]
    .split('\n')
    .map(processNearby);
  let specs = input
    .split("your ticket:")[0]
    .split('\n')
    .map(processSpecs)
    .filter(a => a);
  let mine = processNearby(input
    .split("your ticket:")[1]
    .split("nearby tickets:")[0]);
  return { nearby, specs, mine };
}

function processSpecs(item) {
  if (!item) {
    return;
  }
  let name = item.split(':')[0];
  let vals = item.split(':')[1];
  vals = vals.split('or').map(a => {
    let match = a.match(/(\d+)-(\d+)/);
    return { a: match[1] * 1, b: match[2] * 1 };
  });
  return { name, vals };
}

function processNearby(item) {
  return item.split(',').map(a => a * 1);
};

function _ANSWER_1_INTERNAL(input)
{
  function valueInvalid(field) {
    for (let spec of input.specs) {
      for (let val of spec.vals) {
        if (val.a <= field && val.b >= field) {
          return false;
        }
      }
    }
    return true;
  }

  let bustedTickets = 0;
  let bustedValues = [];
  let goodTickets = [];
  for (let i = 0; i < input.nearby.length; i++) {
    let tick = input.nearby[i];
    let valid = true;
    for (let field of tick) {
      if (valueInvalid(field)) {
        bustedTickets++;
        bustedValues.push(field);
        valid = false;
        break;
      }
    }
    if (valid) {
      goodTickets.push(tick);
    }
  }
  return {
    answer: bustedValues.reduce((a, b) => a + b, 0),
    bustedValues,
    goodTickets
  };
}

function _ANSWER_1(input) {
  return _ANSWER_1_INTERNAL(input).answer;
}

function _ANSWER_2(input)
{
  let ANSWER_1 = _ANSWER_1_INTERNAL(input);
  function invalidForValue(spec, value) {
    let found = true;
    for (let i = 0; i < spec.vals.length; i++) {
      let val = spec.vals[i];
      if (val.a <= value && val.b >= value) {
        // console.log('found');
        found = false;
      }
    }
    return found;
  }

  let invalids = new Map();
  let TICK_LEN = ANSWER_1.goodTickets[0].length;
  for (let i = 0; i < TICK_LEN; i++) {
    invalids.set(i, new Set());
    for (let tick of ANSWER_1.goodTickets) {
      let field = tick[i];
      for (let spec of input.specs) {
        if (invalidForValue(spec, field)) {
          // console.log(spec, field, tick, i);
          invalids.get(i).add(spec.name);
        }
      }
    }
  }
  console.log(input);
  let answers = new Map();
  for (let i = 0; i < 1000; i++) {
    for (let spec of input.specs) {
      invalids.forEach((val, key) => {
        if (val.size == input.specs.length - 1 && !val.has(spec.name)) {
          console.log(spec.name, key)
          answers[spec.name] = input.mine[key];
          invalids.forEach((val, key) => val.add(spec.name));
        }
      });
    }
  }

  let tot = 1;
  for (let k in answers) {
    if (k.includes('departure')) {
      // console.log(k, answers);
      tot *= answers[k];
    }
  }
  return tot;
}
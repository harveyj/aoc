#!/usr/bin/env python3
import puzzle, re, itertools, random, networkx as nx

def flatten_list(nested_list):
    return list(itertools.chain(*nested_list))

def parse_input(INPUT):
  def parse_wf(line):
    match = re.match('(\w+){(.*,?)}',line)
    name = match.group(1)
    rules = match.group(2).split(',')
    return (name, rules)
  wf_raw, vals_raw = INPUT.split('\n\n')
  wf = dict(map(parse_wf, wf_raw.split('\n')))
  vars = [raw[1:-1].split(',') for raw in vals_raw.split('\n')]
  return wf, vars

def apply(rules, part):
  rule = 'in'
  while rule not in ['R', 'A']:
    cur_rules = rules[rule]
    for cr in cur_rules:
      if ':' in cr:
        pred, dst = cr.split(':')
        # print('\n'.join(p) + '\nout = ' + pred)
        locals = {}
        exec('\n'.join(part) + '\nout = ' + pred, locals)
        if locals['out']:
          rule = dst
          break
      else:
        rule = cr
        break
  return rule == 'A'

def one(INPUT):
  rules, parts = parse_input(INPUT)
  out = 0
  for p in parts:
    if apply(rules, p):
      out += sum([int(re.findall('\d+', pv)[0]) for pv in p])
  return out

def new_ruleset(rules):
  def invert_criterion(criterion):
    criterion = criterion.split(':')[0]
    if '>' in criterion:
      criterion = criterion.replace('>', '<=')
    else: 
      criterion =  criterion.replace('<', '>=')
    return criterion

  def adjust_criterion(criterion):
    criterion = criterion.split(':')[0]
    if '>' in criterion:
      var, mag = criterion.split('>')
      mag = int(mag)+1
      return var + '>=' + str(mag)
    elif '<' in criterion: 
      var, mag = criterion.split('<')
      mag = int(mag)-1
      return var + '<=' + str(mag)
    return criterion

  # key = tgt, val = [(criteria, src), ...]
  inverse_rules = {}
  G = nx.MultiDiGraph()
  for dst in list(rules.keys()) + ['R', 'A']:
    G.add_node(dst)
    sources = []
    for src, criteria in rules.items():
      for i, criterion in enumerate(criteria):
        if ':' in criterion:
          tgt = criterion.split(':')[1]
        else:
          tgt = criterion
        if tgt == dst:
          # if tgt == 'A': print(i, list(reversed(criteria[:i+1])))
          inv_rules = [adjust_criterion(criterion)] + list(map(invert_criterion, list(reversed(criteria[:i]))))
          if inv_rules[0] == tgt: inv_rules = inv_rules[1:]              
          sources.append((inv_rules, src))
          G.add_edge(dst, src, rules=inv_rules)
          # print(dst, src, i,  inv_rules)
    inverse_rules[dst] = sources

  ruleset = []
  xmas = 'xmas'

  for path in nx.all_simple_edge_paths(G, source='A', target='in'):
    all_rules = flatten_list([G.get_edge_data(src_node, dst_node, id)['rules'] for src_node, dst_node, id in path])
    all_rules = [rule for rule in all_rules if '=' in rule]
    filtered = {key: [rule for rule in all_rules if key in rule] for key in xmas}
    maxes = {key: None for key in xmas}
    mins = {key: None for key in xmas}
    for key in xmas:
      maxes[key] = min([4000] + [int(rule.split('=')[1]) for rule in filtered[key] if '<' in rule])
      mins[key] = max([1] + [int(rule.split('=')[1]) for rule in filtered[key] if '>' in rule])
    ruleset.append({key: (mins[key], maxes[key]) for key in xmas})
  return ruleset

def two(INPUT):
  rules, _ = parse_input(INPUT)
  ruleset = new_ruleset(rules)
  # print(ruleset)

  # Test rig
  for j in range(10):
    ints = [random.randint(1, 4000) for i in range(4)]
    vars = ['xmas'[i] + '=' + str(val) for i, val in enumerate(ints)]
    method_one = apply(rules, vars)
    method_two_all = {}
    for j, rule in enumerate(ruleset):
      method_two_all[j] = True
      for i, key in enumerate('xmas'):
        if not rule[key][0] <= ints[i] <= rule[key][1]:
          method_two_all[j] = False
    method_two = True in method_two_all.values()
    if method_one != method_two:
      print('MISMATCH ', vars, method_one, method_two)

  out = 0
  for rule in ruleset:
    passes = 1
    for code in 'xmas':
      passes *= rule[code][1]+1 - rule[code][0]
    out += passes
  return out

p = puzzle.Puzzle("19")
# p.run(one, 0)
p.run(two, 0)

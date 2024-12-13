import puzzle
from collections import defaultdict

# Part 1

def process_input(intext):
  start_text, inserts_text = '\n'.join(intext).split("\n\n")
  inserts = {tuple(a.split(" -> ")[0]): a.split(" -> ")[1]
   for a in inserts_text.split("\n")}
  return list(start_text), inserts

def step(in_text, inserts):
  out_text = []
  for i in range(len(in_text) - 1):
    c = in_text[i]
    d = in_text[i+1]
    insert = inserts.get((c,d), None)
    out_text.append(c)
    if insert:
      out_text.append(insert)
  out_text.append(in_text[-1])
  return out_text

def one(intext):
  text, inserts = process_input(intext)

  for i in range(10):
    text = step(text, inserts)
    # print("".join(text))

  hist = defaultdict(int)
  for c in text:
    hist[c] += 1

  min_char = 'N'
  max_char = 'N'
  for k, v in hist.items():
    if v > hist[max_char]:
      max_char = k
    if v < hist[min_char]:
      min_char = k
  return hist[max_char] - hist[min_char]

### Part 2
def process_input2(intext):
  start_text, inserts_text = '\n'.join(intext).split("\n\n")
  inserts = {}
  for l in inserts_text.split('\n'):
    ab, c = l.split(' -> ')
    a, b = tuple(ab)
    inserts[(a,b)] = [(a, c), (c, b)]

  return list(start_text), inserts

def two(intext):
  text, inserts = process_input2(intext)
  one_bi_counts = defaultdict(int)
  for i in range(len(text) - 1):
    one_bi_counts[(text[i], text[i+1])] += 1
  # print(one_bi_counts)

  last = text[-1]
  text_bi = [(text[i], text[i+1])for i in range(len(text)-1)]
  bi_counts = {bi: text_bi.count(bi) for bi in text_bi}
  # print(inserts)
  for i in range(40):
    new_bi_counts = defaultdict(int)
    for bi, bi_count in bi_counts.items():
      if inserts[bi]:
        for insert in inserts[bi]:
          new_bi_counts[insert] += bi_count
      else:
        new_bi_counts[bi] += bi_count
    bi_counts = new_bi_counts
  # print(bi_counts)
  char_counts = defaultdict(int)
  for k, v in bi_counts.items():
    char_counts[k[0]] += v
  char_counts[last] += 1
  min_char = 'N'
  max_char = 'N'
  for k, v in char_counts.items():
    if v > char_counts[max_char]:
      max_char = k
    if v < char_counts[min_char]:
      min_char = k
  return char_counts[max_char] - char_counts[min_char]

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "14")

  p.run(one, 0) 
  p.run(two, 0) 
import copy

class Puzzle(object):
  def __init__(self, year, id):
    self.id = id
    self.inputs = []
    raw_inputs = open(year + '/inputs/' + id + '.txt').read().split('\n\n\n')
    for inval in raw_inputs:
      self.inputs.append([l for l in inval.split('\n') if not l[:2] == '//'])

  def run(self, fn, input_id, user_input=None, **kwarg):
    if user_input:
      answer = fn(self.inputs[input_id], copy.copy(user_input), **kwarg)
    else: 
      answer = fn(self.inputs[input_id], **kwarg)
    print("ANSWER", answer)
    return answer

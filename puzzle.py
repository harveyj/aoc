import copy, time

class Puzzle(object):
  def __init__(self, year, id):
    self.id = id
    self.inputs = []
    raw_inputs = open(year + '/inputs/' + id + '.txt').read().split('\n\n\n')
    for inval in raw_inputs:
      self.inputs.append([l for l in inval.split('\n') if not l[:2] == '//'])

  def run(self, fn, input_id, user_input=None, timed=False, **kwarg):
    if user_input:
      answer = fn(self.inputs[input_id], copy.copy(user_input), **kwarg)
    else: 
      start_time = time.time()
      answer = fn(self.inputs[input_id], **kwarg)
      end_time = time.time()
      if timed: print(f'time: {((end_time-start_time)*1000000//1000)}ms')
    return answer

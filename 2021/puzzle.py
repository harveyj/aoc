import copy

class Puzzle(object):
  def __init__(self, id):
    self.id = id
    self.inputs = open('input' + id + '.txt').read().split('\n\n\n')

  def run(self, fn, input_id, user_input=None, **kwarg):
    if user_input:
      answer =  fn(self.inputs[input_id], copy.copy(user_input), **kwarg)
    else: 
      answer = fn(self.inputs[input_id], **kwarg)
    print("ANSWER", answer)
    return answer

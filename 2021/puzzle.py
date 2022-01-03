import copy

class Puzzle(object):
  def __init__(self, id):
    self.id = id
    self.inputs = open('input' + id + '.txt').read().split('\n\n\n')

  def run(self, fn, input_id, user_input = None):
    if user_input:
      return fn(self.inputs[input_id], copy.copy(user_input))
    else: 
      return fn(self.inputs[input_id])

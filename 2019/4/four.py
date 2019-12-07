num=0
for i in range(356261,846303):
  adjacent = []
  more_than_two = []

  is_adjacent = False
  is_inc = True
  prev = ''
  for c in str(i):
  	if c == prev: 
  		if c in adjacent:
  			more_than_two.append(c)
  		adjacent.append(c)

  	if c < prev: is_inc = False
  	prev=c

  for char in adjacent:
  	if char not in more_than_two: is_adjacent = True

  if is_adjacent and is_inc: num+=1
print(num)
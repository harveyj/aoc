tot = 0
l=1969
inc = int(l)/3 - 2
print(tot)
while inc > 0:
	tot += inc
	inc = inc / 3 - 2
	print(tot)

tot = 0
for l in open("one-in.txt").readlines():
	inc = int(l)/3 - 2
	print(tot)
	while inc > 0:
		tot += inc
		inc = inc / 3 - 2
		print(tot)
		
print(tot)
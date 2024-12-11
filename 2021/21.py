
INPUT_TEST = (4, 8)
INPUT_FULL = (9, 6)

loc1, loc2 = INPUT_FULL
die = 0
die_rollovers = 0
score1 = 0
score2 = 0

def next_die(die, die_rollovers):
	die += 1
	if die == 101:
		die = 1
		die_rollovers += 1
	return die, die_rollovers

while True:
	roll1, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	roll2, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	roll3, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	loc1 += roll1 + roll2 + roll3
	loc1 -=1
	loc1 %= 10
	loc1 += 1
	score1 += loc1
	print(roll1, roll2, roll3, loc1, score1)
	if score1 >= 1000:
		print(score2*(100*die_rollovers + die))
		break
	roll1, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	roll2, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	roll3, die_rollovers = die, die_rollovers = next_die(die, die_rollovers)
	loc2 += roll1 + roll2 + roll3
	loc2 -=1
	loc2 %= 10
	loc2 += 1
	score2 += loc2
	die = roll3
	print(roll1, roll2, roll3, loc2, score2)

	if score2 >= 1000:
		print(score1*(100*die_rollovers + die))
		break


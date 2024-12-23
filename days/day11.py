

def parse(raw_data):
	return raw_data[0].strip().split()


def process(num):
	if num == '0':
		return ['1']
	half,remainder = divmod(len(num), 2)
	if remainder == 0:
		return[str(int(num[:half])), str(int(num[half:]))]
	return [str(int(num) * 2024)]


def condense(numlist):
	numlist = sorted(numlist)
	i = 0
	while i < len(numlist) - 1:
		val1, ct1 = numlist[i]
		val2, ct2 = numlist[i+1]
		if val1 == val2:
			numlist[i] = (val1, ct1+ct2)
			numlist.pop(i+1)
		else:
			i += 1
	return numlist


def part1(raw_data):
	numlist = parse(raw_data)
	for i in range(25):
		newlist = []
		for num in numlist:
			newlist.extend(process(num))
		numlist = newlist
	return len(numlist)


def part2(raw_data):
	numlist = [(num,1) for num in parse(raw_data)]
	for i in range(75):
		newlist = []
		for num, count in numlist:
			newlist.extend([(n,count) for n in process(num)])
		numlist = condense(newlist)
	return sum([c for (_,c) in numlist])

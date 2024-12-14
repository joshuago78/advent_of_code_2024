

def parse(raw_data):
	rules = []
	updates = []
	for line in raw_data:
		if '|' in line:
			rules.append([int(n) for n in line.strip().split('|')])
		elif ',' in line:
			updates.append([int(n) for n in line.strip().split(',')])
	return rules, updates


def part1(raw_data):
	rules, updates = parse(raw_data)
	answer = 0
	for update in updates:
		for a,b in rules:
			try:
				if update.index(a) > update.index(b):
					break
			except:
				continue
		else:
			midpoint = len(update) // 2
			answer += update[midpoint]
	return answer


def get_fixed(rules, update):
	fixed = False
	for a,b in rules:
		try:
			idxa = update.index(a)
			idxb = update.index(b)
		except:
			continue
		if idxa > idxb:
			update.pop(idxa)
			update.insert(idxb, a)
			fixed = True
	if fixed:
		return get_fixed(rules, update)
	return update


def part2(raw_data):
	rules, updates = parse(raw_data)
	answer = 0
	fixed = []
	for update in updates:
		for a,b in rules:
			try:
				idxa = update.index(a)
				idxb = update.index(b)
			except:
				continue
			if idxa > idxb:
				update.pop(idxa)
				update.insert(idxb, a)
				fixed.append(get_fixed(rules, update))
				break
	for update in fixed:
		midpoint = len(update) // 2
		answer += update[midpoint]
	return answer

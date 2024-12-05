

def parse(raw_data):
	return [[int(i) for i in l.strip().split()] for l in raw_data]


def part1(raw_data):
	data = parse(raw_data)
	answer = 0
	for report in data:
		diffs = [j-i for i, j in zip(report[:-1], report[1:])]
		if all([d > 0 and d <= 3 for d in diffs]) or \
			all([d < 0 and d >= -3 for d in diffs]):
				answer += 1
	return answer


def safe(report):
	diffs = [j-i for i, j in zip(report[:-1], report[1:])]
	if all([d > 0 and d <= 3 for d in diffs]) or \
		all([d < 0 and d >= -3 for d in diffs]):
			return True


def part2(raw_data):
	data = parse(raw_data)
	answer = 0
	for report in data:
		if safe(report):
			answer += 1
		else:
			for i in range(len(report)):
				mod_report = report[:i] + report[i+1:]
				if safe(mod_report):
					answer += 1
					break
	return answer

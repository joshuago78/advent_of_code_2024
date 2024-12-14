import re


def parse(raw_data):
	return raw_data


def part1(raw_data):
	data = parse(raw_data)
	answer = 0
	pattern = re.compile(r"mul\(\d+,\d+\)")
	for line in data:
		matches = re.findall(pattern, line)
		for match in matches:
			a,b = [int(num) for num in match[4:-1].split(',')]
			answer += a * b
	return answer


def part2(raw_data):
	data = parse(raw_data)
	answer = 0
	pattern = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
	do = True
	for line in data:
		matches = re.finditer(pattern, line)
		for match in matches:
			if match.group() == "don't()":
				do = False
			elif match.group() == "do()":
				do = True
			elif do:
				a,b = [int(num) for num in match.group()[4:-1].split(',')]
				answer += a * b
	return answer

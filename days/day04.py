from pprint import pprint


def parse(raw_data):
	horz = [line.strip() for line in raw_data]
	vert = [''.join([line[i] for line in horz]) for i in range(len(horz[0]))]

	diag1 = []
	for i in range(len(horz[0])):
		row = 0
		col = i
		chars = []
		while row < len(vert) and col < len(horz):
			chars.append(horz[row][col])
			row += 1
			col += 1
		diag1.append(''.join(chars))
	for i in range(1,len(vert)):
		row = i
		col = 0
		chars = []
		while row < len(vert) and col < len(horz):
			chars.append(horz[row][col])
			row += 1
			col += 1
		diag1.append(''.join(chars))

	diag2 = []
	for i in range(len(horz[0])-1,-1,-1):
		row = 0
		col = i
		chars = []
		while row < len(vert) and col >= 0:
			chars.append(horz[row][col])
			row += 1
			col -= 1
		diag2.append(''.join(chars))
	for i in range(1,len(vert)):
		row = i
		col = len(horz[0]) - 1
		chars = []
		while row < len(vert) and col > 0:
			chars.append(horz[row][col])
			row += 1
			col -= 1
		diag2.append(''.join(chars))

	return {'h':horz, 'v':vert, 'd1':diag1, 'd2':diag2}


def part1(raw_data):
	data = parse(raw_data)
	answer = 0
	for angle, lines in data.items():
		for num, line in enumerate(lines):
			forward = line.count("XMAS")
			backward = line.count("SAMX")
			answer += forward + backward
	return answer


def get_exes(data):
	exes = []
	for r in range(len(data)-2):
		for c in range(len(data[0])-2):
			x = {
				'd1': ''.join([data[r][c], data[r+1][c+1], data[r+2][c+2]]),
				'd2': ''.join([data[r+2][c], data[r+1][c+1], data[r][c+2]])
			}
			exes.append(x)
	return exes


def part2(raw_data):
	data = [line.strip() for line in raw_data]
	answer = 0
	for x in get_exes(data):
		if x['d1'] == 'MAS' or x['d1'] == 'SAM':
			if x['d2'] == 'MAS' or x['d2'] == 'SAM':
				answer += 1
	return answer
	
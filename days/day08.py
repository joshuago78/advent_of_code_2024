from itertools import combinations


def parse(raw_data):
	height = len(raw_data)
	width = len(raw_data[0].strip())
	antennas = {}
	for r in range(height):
		for c in range(width):
			key = raw_data[r][c]
			if key != '.':
				if key not in antennas.keys():
					antennas[key] = []
				antennas[key].append((r,c))
	return height, width, antennas


def findantinodes(a1, a2):
	rise = a2[0] - a1[0]
	run = a2[1] - a1[1]
	n1 = (a2[0]+rise, a2[1]+run)
	n2 = (a1[0]-rise, a1[1]-run)
	return n1, n2


def in_grid(node, h, w):
	r,c = node
	if r >= 0 and r < h and c >= 0 and c < w:
		return True
	return False


def print_grid(h,w,antset,nodes):
	for r in range(h):
		line = ''
		for c in range(w):
			for key,ants in antset.items():
				if (r,c) in ants:
					line += key
					break
				elif (r,c) in nodes:
					line += '#'
					break
			else:
				line += '.'
		print(line)
	print()


def part1(raw_data):
	h,w,antset = parse(raw_data)
	nodes = []
	for key, ants in antset.items():
		ant_combos = combinations(ants, 2)
		for a1, a2 in ant_combos:
			for node in findantinodes(a1, a2):
				if in_grid(node, h, w):
					nodes.append(node)
	return len(set(nodes))


def findallantinodes(a1, a2, h, w):
	rise = a2[0] - a1[0]
	run = a2[1] - a1[1]
	nodes = [a1, a2]
	new = (a2[0]+rise, a2[1]+run)
	while in_grid(new, h, w):
		nodes.append(new)
		new = (new[0]+rise, new[1]+run)
	new = (a1[0]-rise, a1[1]-run)
	while in_grid(new, h, w):
		nodes.append(new)
		new = (new[0]-rise, new[1]-run)
	return nodes


def part2(raw_data):
	h,w,antset = parse(raw_data)
	nodes = set()
	for key, ants in antset.items():
		ant_combos = combinations(ants, 2)
		for a1, a2 in ant_combos:
			nodes.update(findallantinodes(a1, a2, h, w))
	return len(nodes)

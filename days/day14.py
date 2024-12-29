import re
from functools import reduce


def parse(raw_data):
	data = []
	pattern = r"p=(?P<x0>\d+),(?P<y0>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)"
	for line in raw_data:
		m = re.match(pattern, line)
		data.append({k:int(v) for k,v in m.groupdict().items()})
	return data


def printgrid(grid):
	for y in range(len(grid)):
		line = []
		for x in range(len(grid[0])):
			line.append('.' if grid[y][x] == 0 else str(grid[y][x]))
		print(''.join(line))


def part1(raw_data):
	data = parse(raw_data)
	
	height = 103
	width = 101
	steps = 100

	midx = width // 2
	midy = height // 2
	quads = [0,0,0,0]

	for bot in data:
		x = (bot['x0'] + steps * bot['vx']) % width
		y = (bot['y0'] + steps * bot['vy']) % height
		bot['x'] = x
		bot['y'] = y
		quad = None
		if x > midx:
			if y > midy:
				quad = 3
				quads[3] += 1
			elif y < midy:
				quad = 1
				quads[1] += 1
		elif x < midx:
			if y > midy:
				quad = 2
				quads[2] += 1
			elif y < midy:
				quad = 0
				quads[0] += 1
	safety_factor = reduce(lambda x,y: x*y, quads)
	return safety_factor


def part2(raw_data):
	data = parse(raw_data)
	
	height = 103
	width = 101
	steps = 100

	for i in range(10000):
		grid = [[0]*width for j in range(height)]
		for bot in data:
			x = (bot['x0'] + i * bot['vx']) % width
			y = (bot['y0'] + i * bot['vy']) % height
			grid[y][x] += 1
		ok = True
		for y in range(height):
			for x in range(width):
				if grid[y][x] > 1:
					ok = False
					break
			if not ok:
				break
		if ok:
			print(f'---STEP {i}---')
			printgrid(grid)
		
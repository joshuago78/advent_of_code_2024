

def parse(raw_data):
	grid = [list(l.strip()) for l in raw_data]
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] in '<>v^':
				return grid, [(r,c),]


def rotate(dir):
	match dir:
		case '^':
			return '>'
		case 'v':
			return '<'
		case '<':
			return '^'
		case '>':
			return 'v'


def next_step(grid, steps, obs_hit=[]):
	r1,c1 = steps[-1]
	r2,c2 = r1,c1
	dir = grid[r1][c1]
	# get next coords
	match dir:
		case '^':
			r2 -= 1
		case 'v':
			r2 += 1
		case '<':
			c2 -= 1
		case '>':
			c2 += 1
	# check next is on grid
	if r2 < 0 or r2 == len(grid) or c2 < 0 or c2 == len(grid[0]):
		return False
	# check for obstacles
	if grid[r2][c2] in '#O':
		obs_hit.append((r2,c2))
		grid[r1][c1] = rotate(dir)
		return True
	# move
	grid[r1][c1] = '.'
	grid[r2][c2] = dir
	steps.append((r2,c2))
	return True


def part1(raw_data):
	grid, steps = parse(raw_data)
	while next_step(grid, steps):
		pass
	answer = len(set(steps))
	return answer


def has_loop(grid, steps):
	obs_hit = []
	while next_step(grid, steps, obs_hit):
		# check for loop
		if len(obs_hit) >= 8:
			last2 = obs_hit[-2:]
			prior = obs_hit[:-2]
			for i in range(len(prior)-1):
				if prior[i] == last2[0] and prior[i+1] == last2[1]:
					return True
	return False


def part2(raw_data):
	orig_grid, orig_steps = parse(raw_data)
	while next_step(orig_grid, orig_steps):
		pass
	orig_steps = set(orig_steps)
	answer = 0
	for r,c in orig_steps:
		grid, steps = parse(raw_data)
		if grid[r][c] == '.':
			grid[r][c] = 'O'
			if has_loop(grid, steps):
				answer += 1
			grid[r][c] = '.'
	return answer

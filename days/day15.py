

def parse(raw_data):
	split = raw_data.index('\n')
	moves = ''.join(line.strip() for line in raw_data[split+1:])
	grid = [list(line.strip()) for line in raw_data[:split]]
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] == '@':
				botpos = (r,c)
				return grid, moves, botpos


def add2tup(tupleA,tupleB):
	return tuple(map(lambda a,b: a+b, tupleA, tupleB))


def move_bot(grid, botpos, movedir):
	MOVES = {
		'^': (-1,0),
		'v': (1,0),
		'<': (0,-1),
		'>': (0,1)
	}
	r,c = botpos
	move = MOVES[movedir]
	while r < len(grid) and c < len(grid[0]):
		r,c = add2tup((r,c), move)
		if grid[r][c] == '#':
			return botpos
		if grid[r][c] == '.':
			break
	back = (move[0]*-1, move[1]*-1)
	while (r,c) != botpos:
		br, bc = add2tup((r,c), back)
		grid[r][c] = grid[br][bc]
		r,c = br,bc
	grid[r][c] = '.'
	return add2tup(botpos, move)


def calculate_gps(grid):
	gps = 0
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			if col == 'O':
				gps += 100*r + c
	return gps


def print_grid(grid):
	for row in grid:
		print(''.join(row))


def part1(raw_data):
	grid, moves, botpos = parse(raw_data)
	for move in moves:
		botpos = move_bot(grid, botpos, move)
	return calculate_gps(grid)


###############################################################################

MOVES = {
	'^': (-1,0),
	'v': (1,0),
	'<': (0,-1),
	'>': (0,1)
}


class Bot(object):

	def __init__(self, grid, pos):
		self.grid = grid
		self.pos = pos

	def move(self, r, c):
		oldr,oldc = self.pos
		self.grid[r][c] = self
		self.grid[oldr][oldc] = '.'
		self.pos = (r,c)

	def try_to_move(self, direction):
		r,c = add2tup(self.pos, MOVES[direction])
		if self.grid[r][c] == '#':
			return
		if self.grid[r][c] == '.':
			self.move(r,c)
		else:
			box = self.grid[r][c]
			possible, downstream_boxes = box.can_move(direction)
			if possible:
				for box in downstream_boxes:
					box.move(direction)
				self.move(r,c)


class Box(object):

	def __init__(self, grid, p1):
		self.grid = grid
		self.p1 = p1
		self.p2 = (p1[0],p1[1]+1)

	def move(self, direction):
		move = MOVES[direction]
		for r,c in [self.p1, self.p2]:
			self.grid[r][c] = '.'
		r1,c1 = add2tup(self.p1, move)
		self.grid[r1][c1] = self
		self.p1 = (r1,c1)
		r2,c2 = add2tup(self.p2, move)
		self.grid[r2][c2] = self
		self.p2 = (r2,c2)

	def can_move(self, direction):
		r,c = MOVES[direction]
		newp1 = add2tup(self.p1, (r,c))
		newp2 = add2tup(self.p2, (r,c))
		movable_neighbors = []
		for nr, nc in [newp1, newp2]:
			if self.grid[nr][nc] == self or self.grid[nr][nc] == '.':
				continue
			elif self.grid[nr][nc] == '#':
				return False, []
			else:
				box = self.grid[nr][nc]
				if box not in movable_neighbors:
					possible, downstream_neighbors = box.can_move(direction)
					if possible:
						for down_box in downstream_neighbors:
							if down_box not in movable_neighbors:
								movable_neighbors.append(down_box)
					else:
						return False, []
		movable_neighbors.append(self)
		return True, movable_neighbors

	def calculate_gps(self):
		r,c = self.p1
		return 100 * r + c


def parse2(raw_data):
	split = raw_data.index('\n')
	moves = ''.join(line.strip() for line in raw_data[split+1:])
	orig_grid = [list(line.strip()) for line in raw_data[:split]]
	boxes = []
	grid = [['.']*len(line)*2 for line in orig_grid]
	for r in range(len(orig_grid)):
		for c in range(len(orig_grid[0])):
			char = orig_grid[r][c]
			if char in '.#':
				grid[r][c*2] = char
				grid[r][c*2+1] = char
			elif char == '@':
				bot = Bot(grid, (r,c*2))
				grid[r][c*2] = bot
				grid[r][c*2+1] = '.'
			elif char == 'O':
				box = Box(grid, (r,c*2))
				grid[r][c*2] = box
				grid[r][c*2+1] = box
				boxes.append(box)
	return grid, moves, bot, boxes


def print_grid2(grid):
	line = '    '
	for i in range(1, len(grid[0])//5):
		line += f'{i*5: 5}'
	print(line)
	for r,row in enumerate(grid):
		line = [f'{r:02} ']
		c = 0
		while c < len(row):
			if type(row[c]) == Bot:
				line.append('@')
			elif type(row[c]) == Box:
				line.append('[]')
				c += 1
			else:
				line.append(row[c])
			c += 1
		print(''.join(line))


def part2(raw_data):
	grid, moves, bot, boxes = parse2(raw_data)
	#print_grid2(grid)
	#print(f'bot at {bot.pos}')
	for move in moves:
		#print(f'Try to move {move}')
		bot.try_to_move(move)
		#print_grid2(grid)
	total_gps = 0
	for box in boxes:
		total_gps += box.calculate_gps()
	return total_gps

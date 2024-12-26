
FENCE_NEIGHBORS = { 
	# clockwise traversal along outside egdes
	# counterclockwise along internal cutouts
	'-^': [
			(0,1,'-^'), #right
			(0,0,'>|'), #corner
			(-1,1,'|<') #corner
		],
	'-v': [
			(0,-1,'-v'), #left
			(0,0,'|<'), #corner
			(1,-1,'>|') #corner
		],
	'|<': [
			(-1,0,'|<'), #up
			(0,0,'-^'), #corner
			(-1,-1,'-v') #corner
		],
	'>|': [
			(1,0,'>|'), #down
			(0,0,'-v'), #corner
			(1,1,'-^') #corner
		],
}




class Plot(object):

	def __init__(self, row, col, plant):
		self.plant = plant
		self.row = row
		self.col = col
		self.region = None

	def __repr__(self):
		return f'<Plot ({self.row},{self.col}): {self.plant}>'


class Region(object):

	def __init__(self, grid, startr, startc):
		self.plant = grid[startr][startc].plant
		self.grid = grid
		self.plots = set()
		self.fences = []
		self.find_members(startr,startc)

	def add_member(self, row, col):
		plot = self.grid[row][col]
		plot.region = self
		self.plots.add(plot)
		return plot

	def find_members(self, row, col):
		start = self.add_member(row,col)
		queue = [start]
		while queue:
			plot = queue.pop(0)
			for r,c,o in [(0,1,'>|'),(0,-1,'|<'),(1,0,'-v'),(-1,0,'-^')]:
				r,c = (plot.row+r, plot.col+c)
				if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
					self.fences.append((plot.row,plot.col,o))
				else:
					neighbor = self.grid[r][c]
					if neighbor.region is None and neighbor.plant == self.plant:
						queue.append(self.add_member(r,c))
					elif neighbor.region != self:
						self.fences.append((plot.row,plot.col,o))

	def area(self):
		return len(self.plots)

	def perimeter(self):
		return len(self.fences)

	def price(self):
		return self.area() * self.perimeter()

	def count_sides(self):
		sides = 0
		full_traversed = []
		while set(full_traversed) != set(self.fences):
			remainder = list(set(self.fences) - set(full_traversed))
			traversed = [remainder[0],]
			found_next = True
			while found_next:
				found_next = False
				r,c,o = traversed[-1]
				for index, edge in enumerate(FENCE_NEIGHBORS[o]):
					neighbor = (r+edge[0], c+edge[1], edge[2])
					if neighbor in self.fences and neighbor not in traversed[1:]:
						traversed.append(neighbor)
						found_next = True
						if index > 0:
							sides += 1
						break
				if len(traversed) > 1 and traversed[-1] == traversed[0]:
					break
			full_traversed.extend(traversed)
		return sides

	def bulk_price(self):
		return self.area() * self.count_sides()



def parse(raw_data):
	grid = []
	for r, row in enumerate(raw_data):
		grid.append([])
		for c, char in enumerate(row.strip()):
			grid[r].append(Plot(r,c,char))
	return grid


def part1(raw_data):
	grid = parse(raw_data)
	regions = []
	for r,row in enumerate(grid):
		for c,plot in enumerate(row):
			if plot.region is None:
				regions.append(Region(grid,r,c))
	return sum([region.price() for region in regions])


def part2(raw_data):
	grid = parse(raw_data)
	regions = []
	for r,row in enumerate(grid):
		for c,plot in enumerate(row):
			if plot.region is None:
				regions.append(Region(grid,r,c))
	#for region in regions:
	#	print(f'Region {region.plant}: {region.area()} * {region.count_sides()} = {region.bulk_price()}')
	return sum([region.bulk_price() for region in regions])

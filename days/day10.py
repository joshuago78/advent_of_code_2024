

def parse(raw_data):
	grid = [[int(c) for c in row.strip()] for row in raw_data]
	trailheads = [(r,c) for c in range(len(grid[0])) for r in range(len(grid)) if grid[r][c]==0]
	return grid, trailheads


def score(grid, trailhead, rate=False):
	reachable_peaks = set()
	rating = 0
	nodes = [trailhead]
	while nodes:
		r,c = nodes.pop()
		if grid[r][c] == 9:
			reachable_peaks.add((r,c))
			rating += 1
		else:
			for d in [(1,0),(-1,0),(0,1),(0,-1)]:
				r2, c2 = (r+d[0], c+d[1])
				if r2 >= 0 and r2 < len(grid) and c2 >= 0 and c2 < len(grid[0]):
					if grid[r2][c2] == grid[r][c] + 1:
						nodes.append((r2,c2))
	return rating if rate else len(reachable_peaks)


def part1(raw_data):
	grid, trailheads = parse(raw_data)
	answer = sum([score(grid, trailhead) for trailhead in trailheads])
	return answer


def part2(raw_data):
	grid, trailheads = parse(raw_data)
	answer = sum([score(grid, trailhead, rate=True) for trailhead in trailheads])
	return answer

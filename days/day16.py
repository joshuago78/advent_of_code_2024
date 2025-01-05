from collections import OrderedDict
from pprint import pprint


DIRS = {
	'>': {'step': (0,1), 'opp': '<'},
	'<': {'step': (0,-1), 'opp': '>'},
	'v': {'step': (1,0), 'opp': '^'},
	'^': {'step': (-1,0), 'opp': 'v'}
}


def parse(raw_data):
	grid = [[' ' if c=='.' else c for c in l.strip() ] for l in raw_data]
	start = (len(grid)-2, 1)
	end = (1, len(grid[0])-2)
	return grid, start, end


def print_grid(grid, path=None):
	if not path:
		for line in grid:
			print(line)
		return
	for r, row in enumerate(grid):
		line = []
		for c, col in enumerate(row):
			line.append(path.get((r,c), col))
		print(''.join(line))


def possible_moves(grid, current, current_cost):
	cr,cc,cp = current
	neighbors = []
	for np,nvals in DIRS.items():
		# skip opposite direction
		if cp == nvals['opp']:
			continue
		
		nr, nc = cr+nvals['step'][0], cc+nvals['step'][1]
		# check for walls
		if grid[nr][nc] == '#':
			continue
		if np == cp:
			neighbors.append(((nr,nc,np),1+current_cost))
		else:
			neighbors.append(((cr,cc,np),1000+current_cost))
	return neighbors


def build_path(explored, start, end):
	print(f'length explored = {len(explored)}')
	path = {(end[0],end[1]):'E'}
	nodes = set()
	score = float('inf')
	for r,c,p in explored.keys():
		if r==end[0] and c==end[1]:
			print(f'found end in explored {r},{c},{p}')
			cost = explored[(r,c,p)]['cost']
			if cost < score:
				score = cost
				nodes = set(explored[(r,c,p)]['from'])
			elif cost == score:
				nodes.update(set(explored[(r,c,p)]['from']))
	while nodes:
		r,c,p = nodes.pop()
		parents = [node for node in explored[(r,c,p)]['from'] if node not in path.keys()]
		nodes.update(set(parents))
		path[(r,c)] = 'S' if (r,c,p) == start else p
	return path, score


def process(raw_data):
	# Step 0 - set up
	grid, start, end = parse(raw_data)
	start = (start[0],start[1],'>')
	explored = OrderedDict()
	unexplored = OrderedDict()
	unexplored[start] = {'cost': 0, 'from': []}

	# Main loop to process nodes from unexplored and add to explored
	while unexplored:
		current,curvals = unexplored.popitem(0)
		
		# Step 1 - validate next node from list
		# Step 1a - check if node already explored
		altvals = explored.get(current)
		if altvals:
			if curvals['cost'] < altvals['cost']:
				altvals['cost'] = curvals['cost']
				altvals['from'] = curvals['from']
			elif curvals['cost'] == altvals['cost']:
				altvals['from'].extend(curvals['from'])
			continue
		# Step 1b - also check oppostie direction; don't bother going wrong way
		opp = (current[0],current[1],DIRS[current[2]]['opp'])
		oppvals = explored.get(opp)
		if oppvals:
			if curvals['cost'] > oppvals['cost']:
				continue
		# Step 1c - add to explored list
		explored[current] = curvals

		# Step 2 - add new nodes to unexplored list
		# Step 2a - get all possible moves (forward & rotate, no walls or u-turns)
		for nxt,nxtcost in possible_moves(grid, current, curvals['cost']):
			
			# Step 2b - skip if already explored in opp dir at cheaper cost
			opp = (nxt[0],nxt[1],DIRS[nxt[2]]['opp'])
			oppvals = explored.get(opp)
			if oppvals:
				if oppvals['cost'] < nxtcost:
					continue
			# Step 2c - do the same for unexplored nodes
			oppvals = unexplored.get(opp)
			if oppvals:
				if oppvals['cost'] < nxtcost:
					continue
			
			# Step 2d - if already explored, compare costs
			altvals = explored.get(nxt)
			if altvals:
				# if cheaper than already explored, replace it
				if nxtcost < altvals['cost']:
					altvals['cost'] = nxtcost
					altvals['from'] = [current]
				# if same cost, add to possible sources
				elif nxtcost == altvals['cost']:
					altvals['from'].append(current)
			# Step 2e - do same for unexplored list
			altvals = unexplored.get(nxt)
			if altvals:
				# if cheaper than already explored, replace it
				if nxtcost < altvals['cost']:
					altvals['cost'] = nxtcost
					altvals['from'] = [current]
				# if same cost, add to possible sources
				elif nxtcost == altvals['cost']:
					altvals['from'].append(current)
			else:
				# Step 2f - if not in either list, add to unexplored
				unexplored[nxt] = {'cost': nxtcost, 'from': [current]}

	# Step 3 - construct all paths starting from end, using parents	
	# +Also get cost from end node
	path, cost = build_path(explored, start, end)
	print_grid(grid, path)
	return path, cost


def part1(raw_data):
	path, cost = process(raw_data)
	return cost

def part2(raw_data):
	path, cost = process(raw_data)
	return len(path)
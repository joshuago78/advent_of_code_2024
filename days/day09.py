

def parse(raw_data):
	return raw_data[0].strip()


def convert(diskmap):
	blocks = []
	semaphore = 'file'
	filenum = 0
	for char in diskmap:
		size = int(char)
		if semaphore == 'file':
			blocks.extend([str(filenum)] * size)
			filenum += 1
			semaphore = 'freespace'
		else:
			blocks.extend('.' * size)
			semaphore = 'file'
	return blocks, filenum-1



def get_last_file(blocks, start=None):
	i = len(blocks) - 1 if start is None else start
	while blocks[i] == '.':
		i -= 1
	return i


def get_first_space(blocks, start=0):
	while '.' not in blocks[start]:
		start += 1
	return start


def compact(blocks):
	f =  get_first_space(blocks)
	b = get_last_file(blocks)
	while f < b:
		blocks[f] = blocks[b]
		blocks[b] = '.'
		f = get_first_space(blocks, f)
		b = get_last_file(blocks, b-1)
	return blocks


def checksum(blocks):
	return sum([i * int(n) for i,n in enumerate(blocks) if n != '.'])


def part1(raw_data):
	diskmap = parse(raw_data)
	blocks,_ = convert(diskmap)
	blocks = compact(blocks)
	answer = checksum(blocks)
	return answer


def convert2(diskmap):
	files = []
	spaces = []
	blocks = []
	semaphore = 'file'
	filenum = 0
	index = 0
	for char in diskmap:
		size = int(char)
		if semaphore == 'file':
			files.append((filenum,index,size))
			blocks.extend([str(filenum)] * size)
			filenum += 1
			semaphore = 'space'
		else:
			spaces.append((index,size))
			blocks.extend(['.'] * size)
			semaphore = 'file'
		index += size
	return files,spaces,blocks



def swap(blocks,fidx,spidx,size):
	for i in range(size):
		blocks[spidx+i] = blocks[fidx+i]
		blocks[fidx+i] = '.'
	return blocks


def find_space(blocks, size, limit=None):
	limit = len(blocks) if limit is None else limit
	start = 0
	while start < limit:
		try:
			start = blocks.index('.', start)
			end = start
			while blocks[end] == '.':
				if end + 1 - start == size:
					return start
				end += 1
			start = end
		except:
			return None


def compact2(blocks, filecount):
	#print('|'.join(blocks))
	for filenum in range(filecount,-1,-1):
		fidx = blocks.index(str(filenum))
		size = blocks.count(str(filenum))
		spidx = find_space(blocks, size, fidx)
		if spidx is not None:
			swap(blocks,fidx,spidx,size)
			#print('|'.join(blocks))
	return blocks


def part2(raw_data):
	diskmap = parse(raw_data)
	blocks, filecount = convert(diskmap)
	print(f'ORIGINAL\n{'|'.join(blocks)}\n')
	blocks = compact2(blocks, filecount)
	answer = checksum(blocks)
	print(f'COMPACTED\n{'|'.join(blocks)}')
	return answer

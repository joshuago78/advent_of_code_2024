from itertools import product
import re


PART1_OPS = '*+'
PART2_OPS = '*+|'


def parse(raw_data):
	equations = []
	for line in raw_data:
		terms = [int(i) for i in re.split(r'\W+', line.strip())]
		test = terms.pop(0)
		equations.append({'test': test, 'terms':terms})
	return equations


def evaluate(terms, ops):
	if len(ops) == 0:
		return terms[0]
	op = ops.pop(0)
	if op == '*':
		new = terms.pop(0) * terms.pop(0)
	elif op == '+':
		new = terms.pop(0) + terms.pop(0)
	else:
		new = int(f'{terms.pop(0)}{terms.pop(0)}')
	terms.insert(0, new)
	return evaluate(terms, ops)


def possible(eq, ops_set):
	num_ops = len(eq['terms']) - 1
	ops_combos = product(ops_set, repeat=num_ops)
	for ops in ops_combos:
		if eq['test'] == evaluate(eq['terms'].copy(), list(ops)):
			return True
	return False


def part1(raw_data):
	equations = parse(raw_data)
	answer = sum([eq['test'] for eq in equations if possible(eq, PART1_OPS)])
	return answer


def part2(raw_data):
	equations = parse(raw_data)
	answer = sum([eq['test'] for eq in equations if possible(eq, PART2_OPS)])
	return answer
	
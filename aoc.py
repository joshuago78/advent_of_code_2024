import argparse
import importlib
import os


DATA_PATH = 'data'


def read_input(day_num, test=False):
	filename = f'day{day_num:02}.txt' if not test else f'day{day_num:02}test.txt'
	path = os.path.join(DATA_PATH, filename)
	with open(path) as datafile:
		return datafile.read()


def get_function(day_num, part_num):
	module = importlib.import_module(f'days.day{day_num:02}')
	function = getattr(module, f'part{part_num}')
	return function


def main(day_num, part_num, test):
	function = get_function(day_num, part_num)
	raw_data = read_input(day_num, test)
	answer = function(raw_data)
	print(f'The solution for day {day_num}, part {part_num} is {answer}')


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("day_num", type=int, help="The day number")
	parser.add_argument("part_num", type=int, choices=[1,2], help="Part 1 or 2")
	parser.add_argument("-t", "--test", action="store_true", help="Use test data")
	args = parser.parse_args()
	main(args.day_num, args.part_num, args.test)



def parse(raw_data):
    set1, set2 = [], []
    for line in raw_data:
        one,two = line.strip().split()
        set1.append(int(one))
        set2.append(int(two))
    return set1, set2


def part1(raw_data):
    set1, set2 = parse(raw_data)
    set1.sort()
    set2.sort()
    answer = sum([abs(set1[x] - set2[x]) for x in range(len(set1))])
    return answer


def part2(raw_data):
    set1, set2 = parse(raw_data)
    set1.sort()
    set2.sort()
    count = set2.count(set1[0])
    product = set1[0] * count
    answer = product
    for i in range(1, len(set1)):
        if set1[i] == set1[i-1]:
            answer += product
        else:
            count = set2.count(set1[i])
            product = set1[i] * count
            answer += product
    return answer

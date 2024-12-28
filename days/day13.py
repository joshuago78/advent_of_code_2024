import re
import sympy


def parse(raw_data):
    data = []
    line = 0
    while line < len(raw_data) - 2:
        three_line_input = ''.join(raw_data[line:line+3])
        pattern = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)'
        matched = re.match(pattern, three_line_input)
        data.append({
            'ax': int(matched.group(1)),
            'ay': int(matched.group(2)),
            'bx': int(matched.group(3)),
            'by': int(matched.group(4)),
            'px': int(matched.group(5)),
            'py': int(matched.group(6))
        })
        line += 4
    return data


def part1(raw_data):
    data = parse(raw_data)
    total = 0
    for num, machine in enumerate(data, start=1):
        ax,ay,bx,by,px,py = machine.values()
        A = ( px/ax - (py*bx)/(by*ax) ) * ((by*ax)/(by*ax + ay*bx))
        B = (px - A*ax) / bx
        print(f'machine {num}: A={A}, B={B}')
        best = 500
        for A in range(101):
            for B in range(101):
                cost = 3*A + B
                if A*ax + B*bx == px and A*ay + B*by == py and cost < best:
                    best = cost
        if best < 500:
            total += best
        else:
            print(f'cannot win prize {num}')
    return total


def part2(raw_data):
    data = parse(raw_data)
    total = 0
    for num, machine in enumerate(data, start=1):
        ax,ay,bx,by,px,py = machine.values()
        px += int(1e13)
        py += int(1e13)
        A,B=sympy.symbols('A B')
        eq1 = ax * A + bx * B - px
        eq2 = ay * A + by * B - py
        solutions = sympy.solve([eq1,eq2], A, B, dict=True)
        a,b = solutions[0][A], solutions[0][B]
        if a.is_integer and b.is_integer:
            total += a*3 + b
    return total

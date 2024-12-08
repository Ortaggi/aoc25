import re
def parse_numbers():
    file_name = "real.txt"
    # file_name = "test.txt"
    with open(file_name) as f:
        lines = f.readlines()
    l1 = []
    l2 = []
    for l in lines:
        if not l:
            break
        match = re.fullmatch(r"(\d+)   (\d+)\n?", l)
        if not match:
            raise ValueError(f"no match found in regex for line '{l}'")
        groups = match.groups()
        l1.append(int(groups[0]))
        l2.append(int(groups[1]))
    return l1, l2

def part1():
    l1, l2 = parse_numbers()
    l1.sort()
    l2.sort()
    total = 0
    for n in range(len(l1)):
        total += abs(l1[n] - l2[n])
    print(total)

def part2():
    l1, l2 = parse_numbers()
    counts = {}
    for n in l2:
        counts[n] = counts.get(n, 0) + 1
    total = 0
    for n in l1:
        total += n * counts.get(n, 0)
    print(total)

part2()
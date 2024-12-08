def read_data():
    fname = "real"
    with open(f"{fname}.txt") as f:
        lines = f.readlines()
    nums = []
    for l in lines:
        parsed = l.strip()
        if not l:
            break
        parts = parsed.split(' ')
        nums += [[int(n) for n in parts]]
    return nums 

def part1(data):
    points = 0
    for i, l in enumerate(data):
        ok = True
        increasing = None
        prev = l[0]
        for n in l[1:]:
            diff = abs(prev - n)
            if diff < 1 or diff > 3:
                # print(f"line {i} not ok bc diff out of bounds {prev=} {n=}")
                ok = False
                break
            if increasing is None:
                increasing = n > prev
            elif increasing:
                if n < prev:
                    # print(f"line {i} not ok bc increasing but {prev=} > {n=}")
                    ok = False
                    break
            else:
                if n > prev:
                    # print(f"line {i} not ok bc decreasing but {prev=} < {n=}")
                    ok = False
                    break
            prev = n
        if ok:
            points += 1
    print(points)

def part2(data):
    points = 0
    for i, l in enumerate(data):
        for j in range(len(l)):
            """
            if j == 0: i skip first, i initialize prev to #1 adn then I consider all other numbers
            if j != 0: i set prev to #0, then I iterate from 1 to end and skip j
            if j is final: prev = #0, iterate from 1 to end - 1
            """
            ok = True
            increasing = None
            prev = l[0] if j != 0 else l[1]
            for k, n in enumerate(l[1:]):
                if k+1 == j or (j == 0 and k == 0):
                    continue
                diff = abs(prev - n)
                if diff < 1 or diff > 3:
                    # print(f"line {i} not ok bc diff out of bounds {prev=} {n=}")
                    ok = False
                    break
                if increasing is None:
                    increasing = n > prev
                elif increasing:
                    if n < prev:
                        # print(f"line {i} not ok bc increasing but {prev=} > {n=}")
                        ok = False
                        break
                else:
                    if n > prev:
                        # print(f"line {i} not ok bc decreasing but {prev=} < {n=}")
                        ok = False
                        break
                prev = n
            if ok:
                # print(f"line {i} fine if i skip [{l[j]}]")
                points += 1
                break
    print(points)


def main():
    data = read_data()
    part2(data)

main()
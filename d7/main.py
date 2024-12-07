def get_content(test = True):
    fname = 'test.txt' if test else 'real.txt'
    with open(fname) as f:
        return f.read()

def can_equal(parts: list[int], goal: int, cur: int | None = None):
    if len(parts) == 0:
        return cur == goal
    if can_equal(parts[1:], goal, cur*parts[0] if cur else parts[0]):
        return True
    if can_equal(parts[1:], goal, cur+parts[0] if cur else parts[0]):
        return True
    return False

def solvable(total: float, parts: list[int]):
    print(total, parts)
    if len(parts) == 0:
        return total == 1
    if solvable(total / parts[0], parts[1:]):
        return True
    elif solvable(total - parts[0], parts[1:]):
        return True
    return False

def main():
    content = get_content(False)
    data = {}
    for line in content.split('\n'):
        if not line: break
        ps = line.split(':')
        n = int(ps[0])
        ops = [int(v) for v in ps[1].split(' ') if v]
        data[n] = ops
    total = 0
    for k in data:
        if can_equal(data[k], k):
            total += k
    print(total)




main()

"""
try dividing, if it's not an int, it means you need to subract and keep trying
"""
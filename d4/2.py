
def get_content(test: bool = True):
    fname = 'test.txt' if test else 'real.txt'
    with open(fname) as f:
        return f.read().split('\n')

def is_valid(values):
    """
    0 1 
    2 3
    """
    # 0,1,2,3 
    # 0 != 3, 1 != 2 and all have to be m and s
    all_m_and_s = all(v in ['M', 'S'] for v in values)
    diagonals_diff = values[0] != values[3] and values[1] != values[2]
    # print("==")
    # print(values)
    # print(all_m_and_s, diagonals_diff)
    # print("==")
    return all_m_and_s and diagonals_diff

def main():
    content = get_content(False)
    lines = len(content)
    line_len = len(content[0])
    points = 0
    logs = 0
    for y in range(1, lines - 2):
        for x in range(1, line_len - 1):
            if content[y][x] != 'A':
                continue
            # values = [v[ix] for v in content[y-1:y+2] for ix in range(x-1, x+2)]
            values = [v[ix] for v in [content[y-1], content[y+1]] for ix in [x-1, x+1]]
            # if logs < 20:
            #     print(values)
            #     logs += 1

            # # print(values)
            if is_valid(values):
                points += 1
    print(points)

main()
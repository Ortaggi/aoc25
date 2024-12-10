line_count = -1
line_len = -1

def search_path(grid, cury, curx):
    v = grid[cury][curx]
    if v == 9:
        peak = set()
        peak.add((cury, curx))
        return peak
    to_check = []
    if cury - 1 >= 0:
        to_check += [(cury-1, curx)]
    if cury + 1 < line_count:
        to_check += [(cury+1, curx)]
    if curx - 1 >= 0:
        to_check += [(cury, curx - 1)]
    if curx + 1 < line_len:
        to_check += [(cury, curx + 1)]
    peaks = set()
    for point in to_check: 
        y,x = point
        if grid[y][x] != v + 1:
            continue
        # print(f"{v=} {cury=} {curx=} {y=} {x=}")
        peaks = peaks.union(search_path(grid, y, x))
    return peaks

def main():
    global line_count, line_len
    test = False
    fname = "test.txt" if test else "real.txt"
    with open(fname) as f:
        content = f.read()
    lines = [[int(x) for x in l] for l in content.split('\n') if l.strip()]
    # for l in lines:
    #     print(l)
    line_count = len(lines)
    line_len = len(lines[0])
    answer = 0
    for y in range(line_count):
        for x in range(line_len):
            c = lines[y][x]
            if c != 0:
                continue
            peaks = search_path(lines, y, x)
            # print(y, x, peaks)
            answer += len(peaks)
            # print(answer, y, x)
    print(answer)
    answer == 36

main()

"""
given a point you can probably calculate how many peaks it leads to and then reuse that info

"""
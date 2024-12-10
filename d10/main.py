line_count = -1
line_len = -1

def search_path(grid, cury, curx):
    v = grid[cury][curx]
    if v == 9:
        peak = set()
        peak.add((cury, curx))
        return peak
    miny = cury - 1 if cury - 1 >= 0 else cury
    maxy = cury + 1 if cury + 1 < line_len else cury
    minx = curx - 1 if curx - 1 >= 0 else curx
    maxx = curx + 1 if curx + 1 < line_count else curx
    peaks = set()
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if y == cury and x == curx:
                continue
            if grid[y][x] != v + 1:
                continue
            # print(f"{v=} {cury=} {curx=} {y=} {x=}")
            peaks = peaks.union(search_path(grid, y, x))
    # print(peaks)
    return peaks

def main():
    global line_count, line_len
    test = True
    fname = "test.txt" if test else "real.txt"
    with open(fname) as f:
        content = f.read()
    lines = [[int(x) for x in l] for l in content.split('\n') if l.strip()]
    for l in lines:
        print(l)
    line_count = len(lines)
    line_len = len(lines[0])
    answer = 0
    for y in range(line_count):
        for x in range(line_len):
            c = lines[y][x]
            if c != 0:
                continue
            peaks = search_path(lines, y, x)
            print(y, x, peaks)
            answer += len(peaks)
            # print(answer, y, x)
    print(answer)
    answer == 36

main()

"""
given a point you can probably calculate how many peaks it leads to and then reuse that info

"""
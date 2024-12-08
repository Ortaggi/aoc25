class Pos:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Pos(new_y, new_x)

    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Pos(new_y, new_x)

    def ser(self):
        return (self.y, self.x)

line_count: int = -1
line_len: int = -1

def within_boundaries(pos: Pos):
    if pos.y < 0 or pos.y >= line_count:
        return False
    if pos.x < 0 or pos.x >= line_len:
        return False
    return True

def represent(lines, antinodes):
    for y in range(line_count):
        content = ""
        for x in range(line_len):
            if (y,x) in antinodes:
                content += "*"
            else:
                content += lines[y][x]
        print(content)

def main():
    global line_count, line_len
    test = False
    fname = "test.txt" if test else "real.txt"
    with open(fname) as f:
        content = f.read()
    lines = [l for l in content.split('\n') if l.strip()]
    line_count = len(lines)
    line_len = len(lines[0])
    positions = {}
    for y in range(line_count):
        for x in range(line_len):
            c = lines[y][x]
            if c == ".":
                continue
            if c in positions:
                positions[c].append(Pos(y,x))
            else:
                positions[c] = [Pos(y,x)]
    antinodes = set()
    for c in positions:
        all_loc = positions[c]
        if len(all_loc) == 1:
            continue
        for i in range(len(all_loc)):
            antinodes.add(all_loc[i].ser())
            p1 = all_loc[i]
            for y in range(i+1, len(all_loc)):
                p2 = all_loc[y]
                vec = p2 - p1
                an1 = p2 + vec 
                while within_boundaries(an1):
                    antinodes.add(an1.ser())
                    an1 += vec
                an2 = p1 - vec
                while within_boundaries(an2):
                    antinodes.add(an2.ser())
                    an2 -= vec
    # represent(lines, antinodes)
    print(len(antinodes))

main()
"""
now instead of just adding the location 1 step over in each direction I need to add all locations in line in both directions
I thought I could just calculate how many fit in each direction and add that to count, but they might overlap, so I'm not sure how ot avoid that
you could compute the vector + passing point and understand whether anoher line overlaps or there is an intersection with any other line but maybe too mucH??
"""
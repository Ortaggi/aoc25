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
    test = True
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
        for i in range(len(all_loc)):
            p1 = all_loc[i]
            for y in range(i+1, len(all_loc)):
                p2 = all_loc[y]
                vec = p2 - p1
                an1 = p2 + vec 
                if within_boundaries(an1):
                    antinodes.add(an1.ser())
                an2 = p1 - vec
                if within_boundaries(an2):
                    antinodes.add(an2.ser())
    # represent(lines, antinodes)
    print(len(antinodes))

main()
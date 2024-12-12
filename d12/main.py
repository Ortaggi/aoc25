class Game:
    def __init__(self, fname):
        with open(fname) as f:
            content = f.read()
        self.lines = [l for l in content.split('\n') if l.strip()]
        self.line_len = len(self.lines[0])
        self.line_count = len(self.lines)

    def find_regions(self):
        self.regions = {}
        for y in range(self.line_count):
            for x in range(self.line_len):
                c = self.lines[y][x]
                if c not in self.regions:
                    self.regions[c] = set()
                self.regions[c].add((y,x))
        areas = {v: len(self.regions[v]) for v in self.regions}
        print(areas)
        total = 0
        for c in self.regions:
            perimeter = 0
            for pos in self.regions[c]:
                y,x = pos
                edges = 0
                # check left edge
                if x == 0 or (y, x-1) not in self.regions[c]:
                    edges += 1
                if x == self.line_len - 1 or (y, x+1) not in self.regions[c]:
                    edges += 1
                if y == 0 or (y - 1, x) not in self.regions[c]:
                    edges += 1
                if y == self.line_count - 1 or (y + 1, x) not in self.regions[c]:
                    edges += 1
                perimeter += edges
            print(c, perimeter)
            total += areas[c] * perimeter
        print(self.regions)
        print(total)

    def play(self):
        self.find_regions()

game = Game("test1.txt")
game.play()

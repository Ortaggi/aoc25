from functools import reduce

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

    def explore(self, found: set[tuple[int,int]], to_place: set[tuple[int,int]], to_explore: set[tuple[int,int]]) -> set[tuple[int,int]]:
        if not to_explore:
            return found
        cur = to_explore.pop()
        found.add(cur)
        py, px = cur
        to_add = []
        if px - 1>= 0: # search left
            new_p = (py, px-1)
            if new_p in to_place:
                to_add.append(new_p)
        if py - 1 >= 0: # search up
            new_p = (py - 1, px)
            if new_p in to_place:
                to_add.append(new_p)
        if px + 1 <= self.line_len - 1: # search right
            new_p = (py, px + 1)
            if new_p in to_place:
                to_add.append(new_p)
        if py + 1 <= self.line_count - 1: # search down
            new_p = (py + 1, px)
            if new_p in to_place:
                to_add.append(new_p)
        for p in to_add:
            to_explore.add(p)
            to_place.remove(p)
        return self.explore(found, to_place, to_explore)


    def segment_regions(self):
        self.real_regions = {}
        for c in self.regions:
            self.real_regions[c] = []
            to_place: set = self.regions[c].copy()
            while to_place:
                explore = set()
                explore.add(to_place.pop())
                sub_region = self.explore(set(), to_place, explore)
                self.real_regions[c].append(sub_region)

    def compute_areas(self):
        self.areas = {v: len(self.regions[v]) for v in self.regions}

    def compute_perimeters(self):
        self.perimeters = {}
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
            self.perimeters[c] = perimeter

    def compute_total(self):
        # self.total = reduce(lambda acc, el: acc + self.areas[el] * self.perimeters[el], self.areas.keys(), 0)
        total = 0
        for c in self.real_regions:
            regions = self.real_regions[c]
            for i, region in enumerate(regions):
                area = len(region)
                perimeter_lines = set()
                for pos in region:
                    y,x = pos
                    """
                    AAA

                    """
                    # check left edge
                    if x == 0 or (y, x-1) not in region:
                        perimeter_lines.add(('x',x))
                    if x == self.line_len - 1 or (y, x+1) not in region:
                        perimeter_lines.add(('x',x+1))
                    if y == 0 or (y - 1, x) not in region:
                        perimeter_lines.add(('y',y))
                    if y == self.line_count - 1 or (y + 1, x) not in region:
                        perimeter_lines.add(('y',y+1))
                rtotal = area * len(perimeter_lines)
                print(f'reg {i} for char {c}: a {area} p {perimeter_lines}, tot: {rtotal}')
                total += rtotal
        print(total)

    def play(self):
        self.find_regions()
        # self.compute_areas()
        # self.compute_perimeters()
        self.segment_regions()
        self.compute_total()
        # print(self.perimeters)
        # print(self.areas)
        # print(self.total)

game = Game("test1.txt")
game.play()

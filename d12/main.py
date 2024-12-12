from functools import reduce

type Line = tuple[int, int, str]
def hash_from_lines(l1: Line, l2: Line):
    if l1[2] == 'v':
        v = l1; h = l2
    else:
        v = l2; h = l1
    return (h[0],v[1],h,v)
    """
    1,2,h
    1,2,v
    1,2 (punto)
    1,2,h
    1,3,v + 2,3h = 2,3
    1,3 punto
    4,3,h + 3,4,v = 4,4
    y da h, x da v per punto, ordiniamo prima h e poi v
    """

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
                edges = set()
                for pos in region:
                    y,x = pos
                    # check left edge
                    if x == 0 or (y, x-1) not in region:
                        edges.add((y, x, 'v'))
                    if x == self.line_len - 1 or (y, x+1) not in region:
                        edges.add((y, x+1, 'v'))
                    if y == 0 or (y - 1, x) not in region:
                        edges.add((y, x, 'h'))
                    if y == self.line_count - 1 or (y + 1, x) not in region:
                        edges.add((y+1, x, 'h'))
                """
                 0 1 2 3
                0       
                  A A E 
                1       
                  B C D 
                2       
                  E D F 
                3      
                """
                vertices = set()
                while edges:
                    edg = edges.pop()
                    y,x,dir = edg
                    if dir == 'v':
                        # check if edge above to left, above to right, below to left, below to right
                        new_ed = (y, x, 'h')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                        new_ed = (y+1, x, 'h')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                        new_ed = (y, x - 1, 'h')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                        new_ed = (y+1, x - 1, 'h')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                    else:
                        new_ed = (y, x+1, 'v')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                        new_ed = (y-1, x+1, 'v')
                        if new_ed in edges:
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                            # continue
                        new_ed = (y - 1, x, 'v')
                        if new_ed in edges:
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                            # continue
                        new_ed = (y, x, 'v')
                        if new_ed in edges:
                            # print(edg, new_ed)
                            # edges.remove(new_ed)
                            vertices.add(hash_from_lines(edg, new_ed))
                points = {}
                for v in vertices:
                    p = (v[0],v[1])
                    points[p] = points.get(p, 0) + 1
                print(points)
                rtotal = area * len(vertices)
                # print(f'region {i} for c {c}: area {area} peri {vertices}, rtotal: {rtotal}')
                total += rtotal
        return total

    def play(self):
        self.find_regions()
        # self.compute_areas()
        # self.compute_perimeters()
        self.segment_regions()
        return self.compute_total()
        # print(self.perimeters)
        # print(self.areas)
        # print(self.total)

answers = {
    # "test1": 80,
    # "test2": 436,
    # "test3": 1206,
    # "test4": 236,
    "test5": 368
}
for k in answers:
    print(k)
    game = Game(f"{k}.txt")
    total = game.play()
    print(total, answers[k])
    print(answers[k] == total)
    print("=============")
    

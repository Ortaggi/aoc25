from enum import Enum

class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def from_char(c):
        match c:
            case '^':
                return Dir.UP
            case '>':
                return Dir.RIGHT
            case '<':
                return Dir.LEFT
            case 'v':
                return Dir.DOWN
            case _:
                raise ValueError(f"invalid dir {c}")

    def rotate(self):
        match self:
            case Dir.UP:
                return Dir.RIGHT
            case Dir.RIGHT:
                return Dir.DOWN
            case Dir.DOWN:
                return Dir.LEFT
            case Dir.LEFT:
                return Dir.UP


def get_content(test = True):
    fname = 'test.txt' if test else 'real.txt'
    with open(fname) as f:
        return f.read()


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.lines_count = len(lines)
        self.line_len = len(lines[0])
        self.gsigns = ["^", ">", "<", "v"] 
        self.visited = set()
        self.find_guard_pos_and_dir(self.gsigns)
        self.game_over = False

    def find_guard_pos_and_dir(self, cs):
        for y in range(self.lines_count): 
            for x in range(self.line_len):
                if self.lines[y][x] in cs:
                    self.dir = Dir.from_char(self.lines[y][x])
                    self.pos = (y,x)
                    return
        raise ValueError("did not find char I searched for")

    def move_guard(self):
        match self.dir:
            case Dir.UP:
                self.move_up()
            case Dir.DOWN:
                self.move_down()
            case Dir.LEFT:
                self.move_left()
            case Dir.RIGHT:
                self.move_right()
        self.dir = self.dir.rotate()


    def is_obstacle(self, c):
        return c == "#"

    def hash_pos(self, pos):
        return pos

    def move_left(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x - 1, -1 , -1):
            if self.is_obstacle(self.lines[cur_y][x]):
                break
            self.pos = (cur_y, x)
            self.visited.add(self.hash_pos(self.pos))
            if x == 0:
                self.game_over = True
            
    def move_right(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x + 1, self.line_len):
            if self.is_obstacle(self.lines[cur_y][x]):
                break
            self.pos = (cur_y, x)
            self.visited.add(self.hash_pos(self.pos))
            if x == self.line_len - 1:
                self.game_over = True
            
    def move_down(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y + 1, self.lines_count):
            if self.is_obstacle(self.lines[y][cur_x]):
                break
            self.pos = (y, cur_x)
            self.visited.add(self.hash_pos(self.pos))
            if y == self.lines_count - 1:
                self.game_over = True
            
    def move_up(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y - 1, -1 , -1):
            if self.is_obstacle(self.lines[y][cur_x]):
                break
            self.pos = (y, cur_x)
            self.visited.add(self.hash_pos(self.pos))
            if y == 0:
                self.game_over = True
            

    def debug(self):
        for y in range(self.lines_count):
            chars = ""
            for x in range(self.line_len):
                if self.hash_pos((y,x)) in self.visited:
                    chars += "X"
                else:
                    chars += self.lines[y][x]
            print(chars)

    def play(self):
        self.visited.add(self.hash_pos(self.pos))
        while not self.game_over:
            self.move_guard()
        print(len(self.visited))
        # self.debug()


def main():
    content = get_content(False)
    grid = Grid(content.split('\n'))
    grid.play()




"""
use a set to keep all positions visited in form "x;y", gets initialized with starting position of g
on each turn iterate in direction that guard is moving in from current_pos(+-1) to border, if step
does not contain obstacle then you add that to hmap of visited and update current guard pos
if the guard visits an edge position while heading outwards, then it's over
"""
main()
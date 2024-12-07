from enum import Enum

test = False
f = None
first_pos = None
    
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

    def to_char(self):
        match self:
            case Dir.UP:
                return "^"
            case Dir.DOWN:
                return "v"
            case Dir.RIGHT:
                return ">"
            case Dir.LEFT:
                return "<"



def get_content(test = True):
    fname = 'test.txt' if test else 'real.txt'
    with open(fname) as f:
        return f.read()

def is_obstacle(c: str) -> bool:
    return c == "#"

def hash_pos(pos: tuple):
    return pos

def hash_dir_and_pos(dir: Dir, pos: tuple) -> str:
    return f"{dir.value}|{pos}"


class Grid:
    def __init__(self, lines, base_loop = None, add_blk_pos = None, prev_visited = None):
        self.lines = lines
        self.lines_count = len(lines)
        self.line_len = len(lines[0])
        self.gsigns = ["^", ">", "<", "v"] 
        self.prev_visited = prev_visited
        self.visited = set()
        self.find_guard_pos_and_dir(self.gsigns)
        global first_pos
        if first_pos is None:
            first_pos = self.pos
        self.game_over = False
        self.block_positions = set()
        self.base_loop = set()
        self.add_blk_pos = add_blk_pos
        # if base_loop is None:
        #     self.base_loop = set()
        # else:
        #     self.base_loop = base_loop.copy()
        self.checked = set()

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
        if self.game_over:
            return False
        chash = hash_dir_and_pos(self.dir, self.pos)
        # print(chash)
        if chash in self.base_loop:
            return True
        self.base_loop.add(chash)
        self.dir = self.dir.rotate()
        return False


    def find_obs_left(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x - 1, -1 , -1):
            if is_obstacle(self.lines[cur_y][x]):
                return (cur_y, x)
        return None
            
    def find_obs_right(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x + 1, self.line_len):
            if is_obstacle(self.lines[cur_y][x]):
                return (cur_y, x) 
        return None
            
    def find_obs_down(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y + 1, self.lines_count):
            if is_obstacle(self.lines[y][cur_x]):
                return (y, cur_x)
        return None
            
    def find_obs_up(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y - 1, -1 , -1):
            if is_obstacle(self.lines[y][cur_x]):
                return (y, cur_x)
        return None

    def move_left(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x - 1, -1 , -1):
            if is_obstacle(self.lines[cur_y][x]):
                return
            self.pos = (cur_y, x)
            self.visited.add(hash_pos(self.pos))
        self.game_over = True
            
    def move_right(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x + 1, self.line_len):
            if is_obstacle(self.lines[cur_y][x]):
                return
            self.pos = (cur_y, x)
            self.visited.add(hash_pos(self.pos))
        self.game_over = True
            
    def move_down(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y + 1, self.lines_count):
            if is_obstacle(self.lines[y][cur_x]):
                return
            self.pos = (y, cur_x)
            self.visited.add(hash_pos(self.pos))
        self.game_over = True
            
    def move_up(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y - 1, -1 , -1):
            if is_obstacle(self.lines[y][cur_x]):
                return
            self.pos = (y, cur_x)
            self.visited.add(hash_pos(self.pos))
        self.game_over = True
            
    def debug(self):
        tmp = {}
        for elem in self.base_loop:
            pts = elem.split('|')
            dir, poss = pts[0], pts[1]
            pospa = poss.split(',')
            y,x = int(pospa[0][1:]), int(pospa[1][:-1])
            tmp[(y,x)] = dir
        # print(tmp.keys())

        for y in range(self.lines_count):
            chars = ""
            for x in range(self.line_len):
                if (y,x) == self.add_blk_pos:
                    chars += "O"
                elif (y,x) == first_pos:
                    chars += "G"
                elif hash_pos((y,x)) in tmp:
                    chars += "+"
                elif hash_pos((y,x)) in self.visited:
                    chars += "X"
                elif hash_pos((y,x)) in self.prev_visited:
                    chars += "P"
                else:
                    chars += self.lines[y][x]
            f.write(chars)
            f.write('\n')
        f.write("\n\n")

    def check_up(self):
        y, x = self.pos
        if y == 0:
            return "go"
        if is_obstacle(self.lines[y-1][x]):
            return "turn"
        return "move"

    def check_right(self):
        y, x = self.pos
        if x == self.line_len - 1:
            return "go"
        if is_obstacle(self.lines[y][x + 1]):
            return "turn"
        return "move"

    def check_down(self):
        y, x = self.pos
        if y == self.lines_count - 1:
            return "go"
        if is_obstacle(self.lines[y+1][x]):
            return "turn"
        return "move"

    def check_left(self):
        y, x = self.pos
        if x == 0:
            return "go"
        if is_obstacle(self.lines[y][x - 1]):
            return "turn"
        return "move"

    def check_next_move(self):
        match self.dir:
            case Dir.UP:
                return self.check_up()
            case Dir.DOWN:
                return self.check_down()
            case Dir.LEFT:
                return self.check_left()
            case Dir.RIGHT:
                return self.check_right()


    def find_obstacle_in_dir(self, dir):
        match dir:
            case Dir.UP:
                return self.find_obs_up()
            case Dir.DOWN:
                return self.find_obs_down()
            case Dir.LEFT:
                return self.find_obs_left()
            case Dir.RIGHT:
                return self.find_obs_right()

    def duplicate(self, new_blk_pos):
        # print(new_blk_pos)
        new_lines = []
        for y in range(self.lines_count):
            new_line = ""
            for x in range(self.line_len):
                if (y,x) == self.pos:
                    c = self.dir.to_char() 
                elif (y,x) == new_blk_pos:
                    c = '#'
                elif self.lines[y][x] in self.gsigns:
                    c = '.'
                else:
                    c = self.lines[y][x]
                new_line += c
            new_lines.append(new_line)

        temp_grid = Grid(new_lines, base_loop=self.base_loop, add_blk_pos=new_blk_pos, prev_visited=self.visited)
        return temp_grid.play_without_placing() # should return bool for if creates loop

    def play_without_placing(self):
        while not self.game_over:
            if self.move_guard():
                # self.debug()
                # print("==========")
                return True
        return False

    def move(self, set_it = True):
        match self.dir:
            case Dir.UP:
                new_pos = (self.pos[0] - 1, self.pos[1])
            case Dir.DOWN:
                new_pos = (self.pos[0] + 1, self.pos[1])
            case Dir.LEFT:
                new_pos = (self.pos[0], self.pos[1] - 1)
            case Dir.RIGHT:
                new_pos = (self.pos[0], self.pos[1] + 1)

        if set_it:
            self.pos = new_pos
            self.visited.add(hash_pos(new_pos))
        else:
            return new_pos

    def play(self):
        next_move = None
        obs_loop = 0
        obs_no_loop = 0
        while True:
            next_move = self.check_next_move()
            if next_move == "go":
                break
            if next_move == "turn":
                chash = hash_dir_and_pos(self.dir, self.pos)
                if chash in self.base_loop:
                    raise SystemError("found a loop without placing ?")
                    break
                else:
                    self.base_loop.add(chash)
                self.dir = self.dir.rotate()
                continue
            dir = self.dir.rotate()
            obs_in_path = self.find_obstacle_in_dir(dir)
            if obs_in_path is None or obs_in_path in self.block_positions:
                self.move()
                continue
            new_obs = self.move(False)
            if new_obs in self.checked or new_obs in self.visited:
                self.move()
                continue
            res = self.duplicate(new_obs)
            if res:
                self.block_positions.add(new_obs)
                obs_loop += 1
            else:
                obs_no_loop += 1
            self.checked.add(new_obs)
            self.move()

        total = 0
        for obs in self.block_positions:
            y, x = obs
            if self.lines[y][x] == '#':
                print("we placed an obs on top of an obs?")
            else:
                total += 1
        print(total)
        print(f"{obs_loop=}, {obs_no_loop=}")
        print(len(self.block_positions))
        """
        gameplay loop needs to become:
        check what next move should be, if it's move (and not turn)
        check if there's a block to the right of where we're going that could create a loop,
        if so try spawning a branch in which a block gets placed in next move.
        the branch goes on until game over or until loop is found.
        if loop is found we save block spot in a set
        after that we execute the original move and repeat until we go to game over (I imagine 
        we never loop by default?) or loop (if assumption is wrong)
    
        """


def main():
    try:
        global f
        f = open("log.txt", "w")
        content = get_content(test)
        grid = Grid(content.split('\n'))
        grid.play()
    except Exception as e:
        f.close()
        raise e




"""
use a set to keep all positions visited in form "x;y", gets initialized with starting position of g
on each turn iterate in direction that guard is moving in from current_pos(+-1) to border, if step
does not contain obstacle then you add that to hmap of visited and update current guard pos
if the guard visits an edge position while heading outwards, then it's over
"""
main()
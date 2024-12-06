from enum import Enum

f = None
    
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
    def __init__(self, lines, base_loop = None):
        self.lines = lines
        self.lines_count = len(lines)
        self.line_len = len(lines[0])
        self.gsigns = ["^", ">", "<", "v"] 
        self.visited = set()
        self.find_guard_pos_and_dir(self.gsigns)
        self.game_over = False
        self.block_positions = set()
        if base_loop is None:
            self.base_loop = set()
        else:
            self.base_loop = base_loop.copy()
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
            if x == 0:
                return None
            
    def find_obs_right(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x + 1, self.line_len):
            if is_obstacle(self.lines[cur_y][x]):
                return (cur_y, x) 
            if x == self.line_len - 1:
                return None
            
    def find_obs_down(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y + 1, self.lines_count):
            if is_obstacle(self.lines[y][cur_x]):
                return (y, cur_x)
            if y == self.lines_count - 1:
                return None
            
    def find_obs_up(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y - 1, -1 , -1):
            if is_obstacle(self.lines[y][cur_x]):
                return (y, cur_x)
            if y == 0:
                return None

    def move_left(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x - 1, -1 , -1):
            if is_obstacle(self.lines[cur_y][x]):
                break
            self.pos = (cur_y, x)
            self.visited.add(hash_pos(self.pos))
            if x == 0:
                self.game_over = True
            
    def move_right(self):
        cur_y, cur_x = self.pos
        for x in range(cur_x + 1, self.line_len):
            if is_obstacle(self.lines[cur_y][x]):
                break
            self.pos = (cur_y, x)
            self.visited.add(hash_pos(self.pos))
            if x == self.line_len - 1:
                self.game_over = True
            
    def move_down(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y + 1, self.lines_count):
            if is_obstacle(self.lines[y][cur_x]):
                break
            self.pos = (y, cur_x)
            self.visited.add(hash_pos(self.pos))
            if y == self.lines_count - 1:
                self.game_over = True
            
    def move_up(self):
        cur_y, cur_x = self.pos
        for y in range(cur_y - 1, -1 , -1):
            if is_obstacle(self.lines[y][cur_x]):
                break
            self.pos = (y, cur_x)
            self.visited.add(hash_pos(self.pos))
            if y == 0:
                self.game_over = True
            
    def debug(self):
        for y in range(self.lines_count):
            chars = ""
            for x in range(self.line_len):
                if hash_pos((y,x)) in self.visited:
                    chars += "X"
                else:
                    chars += self.lines[y][x]
            print(chars)

    def check_up(self):
        y, x = self.pos
        if y == 0:
            return "go"
        if is_obstacle(self.lines[y-1][x]):
            return "turn"
        return "move,right"

    def check_right(self):
        y, x = self.pos
        if x == self.line_len - 1:
            return "go"
        if is_obstacle(self.lines[y][x + 1]):
            return "turn"
        return "move,down"

    def check_down(self):
        y, x = self.pos
        if y == self.lines_count - 1:
            return "go"
        if is_obstacle(self.lines[y+1][x]):
            return "turn"
        return "move,left"

    def check_left(self):
        y, x = self.pos
        if x == 0:
            return "go"
        if is_obstacle(self.lines[y][x - 1]):
            return "turn"
        return "move,up"

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
            case "up":
                return self.find_obs_up()
            case "down":
                return self.find_obs_down()
            case "left":
                return self.find_obs_left()
            case "right":
                return self.find_obs_right()

    def move_in_dir(self, dir: str):
        f.write(f"{self.pos[0]} {self.pos[1]} - {dir}\n")
        match dir:
            case "up":
                self.pos = (self.pos[0] - 1, self.pos[1])
            case "down":
                self.pos = (self.pos[0] + 1, self.pos[1])
            case "left":
                self.pos = (self.pos[0], self.pos[1] - 1)
            case "right":
                self.pos = (self.pos[0], self.pos[1] + 1)

    def duplicate(self, new_blk_pos, logit):
        print(new_blk_pos)
        new_lines = []
        for y in range(self.lines_count):
            new_line = ""
            for x in range(self.line_len):
                try:
                    if (y,x) == self.pos:
                        c = self.dir.to_char() 
                    elif (y,x) == new_blk_pos:
                        c = '#'
                    elif self.lines[y][x] in self.gsigns:
                        c = '.'
                    else:
                        c = self.lines[y][x]
                    new_line += c
                except IndexError as e:
                    print(f"{x=}, {y=}, {new_blk_pos=}")
                    raise e
            if logit:
                pass
                # print(new_line)
            new_lines.append(new_line)

        temp_grid = Grid(new_lines, base_loop=self.base_loop)
        return temp_grid.play_without_placing() # should return bool for if creates loop

    def play_without_placing(self):
        self.visited.add(hash_pos(self.pos))
        while not self.game_over:
            if self.move_guard():
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
        else:
            return new_pos

    def play(self):
        next_move = None
        first = True
        log = 0
        logit = True
        while True:
            next_move = self.check_next_move()
            if first:
                print(next_move)
                first = False
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
            parts = next_move.split(',')
            dir = parts[1]
            obs_in_path = self.find_obstacle_in_dir(dir)
            if log < 20:
                print(f"searching for obs from {self.pos} to {dir}. res {obs_in_path}")
                log += 1
            if obs_in_path is None or obs_in_path in self.block_positions:
                self.move()
                continue
            new_obs = self.move(False)
            print(f"{self.line_len=}, {self.lines_count=}, {new_obs=}")
            res = self.duplicate(new_obs, logit)
            logit = False
            print('duplicated!')
            if res:
                self.block_positions.add(new_obs)
            self.move()

        print(self.block_positions, len(self.block_positions))
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
        content = get_content(False)
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
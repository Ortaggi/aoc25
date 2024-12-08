import re

def parse_input(test):
    fname = "test2.txt" if test else "real.txt"
    with open(fname) as f:
        return f.read()

def part1(input):
    r"mul\((\d{1,3}),(\d{1,3})\)|don\'t\(\)|do\(\)"
    input = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input)
    sum = 0
    for t in input:
        sum += int(t[0]) * int(t[1])
    print(sum)

# pointer to where we are
# another goes from where we are to the end of current scan. If no full word is found you advance first cursor, otherwise you move first cursor to 
def part2(input):
    debug = False
    if debug:
        print(input)
    _tokens = ["mul(\d+,\d+)", "do()", "don't()"]
    parsed = []
    i = 0
    log = 0
    muls = []
    while i < len(input):
        possible_match = input[i] in ["m", "d"]
        if not possible_match:
            i += 1
            continue
        if input[i] == "d":
            if input[i:i+4] == "do()":
                parsed += ["do"]
                i += 4
                if debug:
                    print(f"found do advancing cursor to {i} {input[i]}")
            elif input[i:i+7] == "don't()":
                parsed += ["dont"]
                i += 7
                if debug:
                    print(f"found dont advancing cursor to {i} {input[i]}")
            else:
                i += 1
                continue
        else:
            if input[i:i+4] != "mul(":
                i += 1
                continue
            num1_start = i+4
            y = num1_start
            while 48 <= ord(input[y]) <= 57 and y <= num1_start + 2:
                y += 1
            if y == num1_start:
                i = y
                if debug:
                    print(f"found mul( but no nums adv to {i} {input[i]}")
                continue
            if input[y] != ",":
                i = y
                if debug:
                    print(f"found mul(d but no , adv to {i} {input[i]}")
                continue
            num1 = int(input[num1_start:y])
            num2_start = y+1 # y is ,
            j = num2_start
            while 48 <= ord(input[j]) <= 57 and j <= num2_start + 2:
                j += 1
            if j == num2_start:
                i = j
                if debug:
                    print(f"found mul(d, but no 2nd num adv to {i} {input[i]}")
                continue
            if input[j] != ')':
                i = j
                if debug:
                    print(f"found mul(d,d but no ) adv to {i} {input[i]}")
                continue
            num2 = int(input[num2_start:j])
            mul = f"{num1},{num2}"
            muls += [mul]
            parsed += [num1*num2]
            i = j + 1
            if log < 10:
                print(f"found full mul {mul} adv to {i} {input[i]}")
                log += 1
            if debug:
                print(f"found full mul adv to {i} {input[i]}")
    
    total = 0
    active = True
    for p in parsed:
        if p == "do":
            active = True
        elif p == "dont":
            active = False
        else:
            if active:
                total += p
    
    print("with cust ", len(muls))
    print(muls[:10])
    print(total)
    return muls
        

def main():
    input = parse_input(test=False)
    res = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input)
    muls = []
    for t in res:
        muls += [f"{t[0]},{t[1]}"]
    print("with re ", len(res))
    cmuls = part2(input)
    ex = 0
    for i in muls:
        if ex > 20:
            break
        if i not in cmuls:
            # print(i)
            ex += 1

main()
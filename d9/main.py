from functools import reduce

def decompress(s: str) -> str:
    id = 0
    decompressed = ""
    file = True
    for c in s:
        to_insert = "."
        if file:
            to_insert = str(id)
            id += 1
        file = not file
        decompressed += to_insert * int(c)
    return decompressed
        
def compact(s: str) -> str:
    # maybe there is a more efficient way but for now I'll try this
    # find first space available
    # start from last string char and move it to space
    # if the 2 cursors meet we're done
    tmp = list(s)
    first_space = 0
    last_char = len(tmp)
    while True:
        for i in range(first_space, len(tmp)):
            if tmp[i] == ".":
                first_space = i
                break
        if first_space >= last_char or first_space == 0:
            break
        for i in range(last_char - 1, first_space, -1):
            if tmp[i] != ".":
                last_char = i
                break
        tmp[first_space] = tmp[last_char]
    with open("tmp.txt", "w") as f:
        f.write("".join(tmp))
    return "".join(tmp[:last_char])

def checksum(s: str) -> int:
    return reduce(lambda acc, i: acc + int(s[i]) * i, range(len(s)), 0)

def main():
    test = "2333133121414131402"
    real = True
    if real:
        with open("real.txt") as f:
            test = f.read()
    result = checksum(compact(decompress(test)))
    print(result)

main()
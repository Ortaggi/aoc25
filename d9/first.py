from functools import reduce

def decompress(s: str) -> list[str | int]:
    id = 0
    decompressed = []
    file = True
    for c in s:
        to_insert = ["."]
        if file:
            to_insert = [id]
            id += 1
        file = not file
        decompressed += to_insert * int(c)
    return decompressed
        
def compact(s: list[str | int]) -> list[int]:
    # maybe there is a more efficient way but for now I'll try this
    # find first space available
    # start from last string char and move it to space
    # if the 2 cursors meet we're done
    first_space = 0
    last_char = len(s)
    while True:
        for i in range(first_space, len(s)):
            if s[i] == ".":
                first_space = i
                break
        if first_space >= last_char or first_space == 0:
            break
        for i in range(last_char - 1, first_space, -1):
            if s[i] != ".":
                last_char = i
                break
        s[first_space] = s[last_char]
    # with open("tmp.txt", "w") as f:
    #     f.write("".join(s))
    return s[:last_char]

def checksum(s: list[int]) -> int:
    return reduce(lambda acc, i: acc + s[i] * i, range(len(s)), 0)

def main():
    test = "2333133121414131402"
    real = True
    if real:
        with open("real.txt") as f:
            test = f.read()
    result = checksum(compact(decompress(test)))
    print(result)

main()
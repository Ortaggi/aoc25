from functools import reduce

def decompress(s: str) -> tuple[list[int | str], int]:
    id = 0
    decompressed = []
    file = True
    for c in s:
        if file:
            to_insert = id
            id += 1
        else:
            to_insert = '.'
        file = not file
        decompressed += [to_insert] * int(c)
    return decompressed, id - 1

def compact(s: list[str | int], max_id: int) -> list[int]:
    max_cont_space = -1
    i = len(s) - 1
    while i >= 0:
    # for i in range(len(s) - 1, -1, -1):
        if s[i] == '.':
            i -= 1
            continue
        cur = s[i]
        # print(cur, max_cont_space)
        ncount = 1
        while s[i-ncount] == cur and i - ncount > 0:
            ncount += 1
        if max_cont_space != -1 and ncount > max_cont_space:
            i -= ncount
            continue
        space_found = False
        max_count = -1
        count = -1
        for y in range(0, i):
            if s[y] != '.':
                continue
            count = 1
            while s[y+count] == "." and count < ncount and y+count < len(s) - 1:
                count += 1
            if count < ncount:
                if count > max_count:
                    max_count = count
                continue
            # count == ncount
            s[y:y+count] = [cur] * count
            s[i-count+1:i+1] = ["."] * count
            # print(s)
            space_found = True
            break
        if not space_found and max_count != -1:
            max_cont_space = max_count
        i -= ncount
    return s
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
    # print(s)
    total = 0
    for i in range(len(s)):
        if s[i] == ".":
            continue
        total += s[i] * i
    return total

def main():
    test = "2333133121414131402"
    real = False
    if real:
        with open("real.txt") as f:
            test = f.read()
    decompressed, max_id = decompress(test)
    print(checksum(compact(decompressed, max_id)))

main()
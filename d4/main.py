"""
0,0  0,1  0,2  0,3

1,0  1,1  1,2  1,3

2,0  2,1  2,2  2,3

3,0  3,1  3,2  3,3
"""
seq = [
    # all horizontal possibilities (need to be reversed as well)
    [0,1,2,3],
    [4,5,6,7],
    [8,9,10,11],
    [12,13,14,15],
    # vertical
    [0,4,8,12],
    [1,5,9,13],
    [2,6,10,14],
    [3,7,11,15],
    # diagonals
    [0,5,10,15],
    [3, 6, 9, 12]
]

already_searched = set()

def xmas_in_block(full, indices):
    to_find = "XMAS"
    matches = 0
    debug = []
    for si, s in enumerate(seq):
        match si:
            case 0 | 1 | 2 | 3:
                stype = "h"
            case 4 | 5 | 6 | 7:
                stype = 'v'
            case 8:
                stype = 'dr'
            case 9:
                stype = 'dl'
            case _:
                raise ValueError(f"unhandled si: {si}")
        match = True
        shash = ""
        for i, v in enumerate(s):
            if i == 0:
                shash = f"{indices[v]};{stype}"
                if shash in already_searched:
                    break
            val = full[indices[v]]
            if val != to_find[i]:
                match = False
                break
        if shash in already_searched:
            continue
        already_searched.add(shash)
        if match:
            debug.append(([(indices[z], full[indices[z]]) for z in s ], shash, ' '))
            matches += 1
            continue
        match = True
        for i, v in enumerate(s[::-1]):
            val = full[indices[v]]
            if val != to_find[i]:
                match = False
                break
        if match:
            debug.append(([(indices[z], full[indices[z]]) for z in s ], shash, 'R'))
            matches += 1

    # for d in debug:
    #     print(d)
    return matches

def count_xmas(cont):
    line_len = len(cont[0])
    cont = [x for y in cont for x in y]
    max_offset = 3 * line_len + 3
    total = 0
    for i in range(len(cont) - max_offset):
        if i % line_len >= line_len - 3:
            continue
        indices = [i+x+z*line_len for z in range(4) for x in range(4)]
        values = [cont[i] for i in indices]
        inblk = xmas_in_block(cont, indices)
        # print(inblk)
        total += inblk
    print(total)
            


def get_content(test: bool):
    fname = 'test.txt' if test else 'real.txt'
    with open(fname) as f:
        return f.readlines()

def main():
    content = get_content(False)
    count_xmas(content)

main()
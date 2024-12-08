def get_content(test = True):
    fname = "test.txt" if test else "real.txt"
    with open(fname) as f:
        content = f.read()
    parts = content.split('\n\n')
    before = []
    for line in parts[0].split('\n'):
        lparts = line.split('|')
        before.append((int(lparts[0]),int(lparts[1])))
    to_parse = []
    for line in parts[1].split('\n'):
        to_parse += [[int(p) for p in line.split(',')]]
    return before, to_parse

"""
something is correctly order unless
a number that should come before another number, comes after it
e.g. 13|45
45,11,13 or 45,13,8
the number that comes first, cannot break any rules, since it's first
last # is the most likely to violate contract
"""
def part1():
    before, to_parse = get_content(False)
    ordering = {}
    for el in before:
        b,a = el
        if b in ordering:
            ordering[b].append(a)
        else:
            ordering[b] = [a]
    total = 0
    for seq in to_parse:
        ok = True
        for i in range(len(seq) - 1, -1, -1):
            n = seq[i]
            if n not in ordering:
                continue
            must_come_after = ordering[n]
            for el in must_come_after:
                if el in seq[0:i]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            if len(seq) % 2 == 0:
                raise ValueError("a sequence has even len")
            total += seq[len(seq) // 2]
    print(total)


def part2():
    before, to_parse = get_content(False)
    ordering = {}
    for el in before:
        b,a = el
        if b in ordering:
            ordering[b].append(a)
        else:
            ordering[b] = [a]
    total = 0
    for seq in to_parse:
        ok = True
        for i in range(len(seq) - 1, -1, -1):
            n = seq[i]
            if n not in ordering:
                continue
            must_come_after = ordering[n]
            for el in must_come_after:
                if el in seq[0:i]:
                    ok = False
                    break
            if not ok:
                break
        """
        list of items to reorder
        make another list which will contain the ordered items
        for each of the item to place:
            if it does not need to be before anything:
                slap it at the end and move to the next item to place
            if it needs to come before something:
                if it needs to come before something that is still in to be placed:
                    go to next number, can't place this one
                else:
                    place it in listand go to next item to place

        """
        if ok:
            continue

        to_place = list(seq)
        new_list = []
        while to_place:
            for i in range(len(to_place)):
                elem = to_place[i]
                if elem not in ordering:
                    new_list.insert(0, elem)
                    to_place = without_elem(to_place, i)
                    break
                else:
                    possible = True
                    for af in ordering[elem]:
                        if af in without_elem(to_place, i):
                            possible = False
                            break
                    if possible:
                        new_list.insert(0, elem)
                        to_place.remove(elem)
                        break
                            
        if len(seq) % 2 == 0:
            raise ValueError("a sequence has even len")
        cur = new_list[len(new_list) // 2]
        # print(cur)
        total += cur
    print(total)

def without_elem(array, index):
    arr = []
    for (idx, i) in enumerate(array):
        if idx == index:
            continue
        arr += [i]
    return arr
    
def main():
    part2()

main()
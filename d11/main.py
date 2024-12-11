def count_digits(n: int):
    d = 1
    while n // 10 != 0:
        d += 1 
        n = n // 10
    return d

cache = {}
def main():
    test = "125 17"
    real = "510613 358 84 40702 4373582 2 0 1584"
    stones = [int(v) for v in real.split(' ') if v.strip()]
    print(stones)
    blinks = 75
    for i in range(blinks):
        if i % 5 == 0:
            print(f"blink {i}, stone len {len(stones)}")
        new_stones = []
        for s in stones:
            if s == 0:
                new_stones += [1]
            else: 
                if s in cache:
                    new_stones += cache[s]
                    continue
                digits = count_digits(s)
                if digits % 2 == 0:
                    left = int(s // 10**(digits/2))
                    right = int(s % 10**(digits/2))
                    new_stones += [left, right]
                    cache[s] = [left, right]
                else:
                    new_stones += [s * 2024]
                    cache[s] = [s * 2024]
        stones = new_stones
    print(len(stones))
                


    correct = 55312

main()
"""
if 0 -> 1
if even number of digits -> split into two, remove leading 0s
else multiply for 2024
"""
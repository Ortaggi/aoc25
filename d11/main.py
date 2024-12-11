from collections import UserDict
def count_digits(n: int):
    d = 1
    while n // 10 != 0:
        d += 1 
        n = n // 10
    return d

cache = {}

class DictWithMax(UserDict):
    def __init__(self, mapping):
        self.max = -1
        for k in mapping:
            if k > self.max:
                self.max = k
        super().__init__(mapping)
    
    def __setitem__(self, key, value):
        if key > self.max:
            self.max = key
        super().__setitem__(key, value)


"""
esempio:
1 -> 2024
2024 -> 20 24
20 24 -> 2 0 2 4
2 0 2 4 -> 4048 1 4048 8096

f([1],1) = [2024]
f([1],2) = f([2024], 1) = [20 24]
f([1],3) = f([2024], 2) = f([20 24], 1) = [2 0 2 4]
"""

def transformsnc(n: int, turns: int):
    if turns == 0:
        return 1
    if n == 0:
        return transformsnc(1, turns - 1)
    digits = count_digits(n)
    if digits % 2 == 0:
        left = int(n // 10**(digits/2))
        right = int(n % 10**(digits/2))
        return transformsnc(left, turns - 1) + transformsnc(right, turns - 1)
    return transformsnc(n * 2024, turns - 1)

cache = {}
def transform(n: int, turns: int):
    if turns == 0:
        return 1
    hsh = (n,turns)
    if hsh in cache:
        return cache[hsh]
    if n == 0:
        result = transform(1, turns - 1)
        cache[hsh] = result
        return result
    digits = count_digits(n)
    if digits % 2 == 0:
        left = int(n // 10**(digits/2))
        right = int(n % 10**(digits/2))
        result = transform(left, turns - 1) + transform(right, turns - 1)
        cache[hsh] = result
        return result
    result = transform(n * 2024, turns - 1)
    cache[hsh] = result
    return result

def main():
    test = False
    input = "125 17" if test else "510613 358 84 40702 4373582 2 0 1584"
    stones = [int(v) for v in input.split(' ') if v.strip()]
    blinks = 75
    result = 0
    for s in stones:
        result += transform(s, blinks)
        print(f"done with stone {s}")
    print(result)


main()

# this one is just here for fun, I don't actually know how this algorithm works.

import random

def miller_rabin(n, k=40):

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

while True:
    n = random.randint(1 << 4095 - 1, 1 << 4096 - 1)
    if miller_rabin(n):
        print(n)
        break

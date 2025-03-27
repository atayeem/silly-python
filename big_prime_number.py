from math import sqrt, log10
from itertools import count
from time import time

primes_cache = [2, 3, 5, 7, 11, 13, 19, 23, 29]
divisor_cache = [2, 3, 5, 7]

# wheel of 570570

big_wheel = False
def candidates() -> int:
    global big_wheel
    for num in count(30, 30):
        for add in [1,7,11,13,17,19,23,29]:
            yield num + add
            if big_wheel:
                break
        
        if big_wheel:
            break
    
    print("now using big wheel", primes_cache[-1])
    for num in count(570570, 570570):
        for add in [1] + primes_cache[7:50452]:
            yield num + add
    

def biggify_prime() -> int:
    for n in count(primes_cache[-1] ** 2 - 2, -2):

        is_prime = True

        for p in primes_cache:
            if n % p == 0:
                is_prime = False
        
        if is_prime:
            return n

def gen_primes(use_time: float):
    global big_wheel
    target_time = time() + use_time
    switch_to_big_wheel_time = time() + 1

    i = 0
    for candidate in candidates():
        is_prime = True

        if int(sqrt(candidate)) + 1 > divisor_cache[-1]:
            divisor_cache.append(primes_cache[len(divisor_cache)])
        
        for p in divisor_cache:
            if candidate % p == 0:
                is_prime = False
                break
        
        if is_prime:
            primes_cache.append(candidate)

            i += 1
            if i % 20000 == 0:
                if time() > switch_to_big_wheel_time:
                    big_wheel = True
                
                if time() > target_time:
                    break
        else:
            continue
    
    print(f"{time() - target_time:.2f} seconds over.")
    p = biggify_prime()
    print(f"prime: {p:,}")
    print(f"log score: {log10(p):.3f}")
    with open("logscores.txt", "a") as f:
        f.write(f"{use_time:.1f}: {log10(p):.3f}\n")


gen_primes(60 * 5.0 - 1)

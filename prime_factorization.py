from math import sqrt

primes_cache = [2, 3, 5]

def greatest_prime() -> int:
    return primes_cache[-1]

def candidates(start: int, limit: int) -> int:

    for num in range(start + 2, limit, 2):
        # Wheel of 30 method
        if num % 30 not in [1,7,11,13,17,19,23,29]:
            continue

        yield num

def primes(limit: int, gen=False) -> int:
    if not gen:
        limit = int(sqrt(limit)) + 1

        for prime in primes_cache:
            if prime > limit:
                return
            
            yield prime
        
    # Start generating new primes

    if gen:
        limit += greatest_prime()
    
    for candidate in candidates(primes_cache[-1], limit):
        is_prime = True

        for p in primes(candidate):
            if candidate % p == 0:
                is_prime = False
                break
        
        if is_prime:
            primes_cache.append(candidate)
            yield candidate
        else:
            continue

def get_factors(n) -> bool:
    print(f"{n} = ", end="")
    something_done = True

    while something_done:
        something_done = False
        for prime in primes(n):
            if n % prime == 0:
                n //= prime

                print(str(prime) + "*", end="", flush=True)
                something_done = True
                break
            
            if n == 1:
                break
    
    if n != 1:
        print(str(n))
    else:
        print(chr(8) + " ")
    
    print()

def main():
    all(primes(200000, gen=True))

    while True:
        all(primes(100000, gen=True))

        try:
            n = int(input("Enter a positive integer: "))
            if n < 2:
                raise ValueError

        except ValueError:
            print("Invalid input!\n")
        
        else:
            get_factors(n)
    
main()

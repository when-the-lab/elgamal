import random
import time

def isprime(n):
    """
    check if integer n is a prime
    """
    # make sure n is a positive integer
    n = abs(int(n))
    # 0 and 1 are not primes
    if n < 2:
        return False
    # 2 is the only even prime number
    if n == 2:
        return True
    # all other even numbers are not primes
    if not n & 1:
        return False
    # range starts with 3 and only needs to go up the square root of n
    # for all odd numbers
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def generate_prime(bits=30):
    # Generate a random prime number with the given number of bits.
    while True:
        # By generating a random integer with the given number of bits
        # and setting the lowest bit (LSB) to 1.
        n = random.getrandbits(bits)
        n |= 1
        if isprime(n):
            return n


if __name__ == "__main__":
    start_time = time.time()
    prime = generate_prime()
    end_time = time.time()
    print(f"Generated prime: {prime}")
    print(f"Time taken: {end_time - start_time:.3f} seconds")
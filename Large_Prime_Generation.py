import random
import time


def is_prime(n):
    # Check if n is prime using the Miller-Rabin primality test.
    # Base cases
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True

    # Even numbers (except 2) are not prime
    if n % 2 == 0:
        return False

    # Write n-1 as d * 2^s by factoring powers of 2 from n-1
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Set of bases to use for the Miller-Rabin test
    # These are the bases that have been shown to be sufficient
    # for numbers up to 2^64.
    bases = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    for a in bases:
        if not miller_rabin_test(a, s, d, n):
            return False
    return True


def miller_rabin_test(a, s, d, n):
    # Perform one iteration of the Miller-Rabin test using the given
    # base a, factored form of n-1 s and d, and the number n to test.
    x = pow(a, d, n)
    if x == 1:
        # a^d = 1 (mod n), n may be prime
        return True
    for i in range(s):
        if x == n - 1:
            # a^(d*2^r) = -1 (mod n), n may be prime
            return True
        x = pow(x, 2, n)
    return False


def generate_prime(bits=1026):
    # Generate a random prime number with the given number of bits.
    while True:
        # By generating a random integer with the given number of bits
        # and setting the lowest bit (LSB) to 1.
        n = random.getrandbits(bits)
        n |= 1
        if is_prime(n):
            return n


if __name__ == "__main__":
    start_time = time.time()
    prime = generate_prime()
    end_time = time.time()
    print(f"Generated prime: {prime}")
    print(f"Time taken: {end_time - start_time:.3f} seconds")

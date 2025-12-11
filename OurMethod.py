import math
import random
import Large_Prime_Generation
import time
from sympy.ntheory import factorint
import sympy

def generate_update():
    # Choose a large prime p
    p = Large_Prime_Generation.generate_prime()

    # Choose a primitive root alpha
    alpha = random.randint(2, p - 2)
    while pow(alpha, (p - 1) // 2, p) == 1:
        alpha = random.randint(2, p - 2)

    # Choose a random private key x
    x = random.randint(1, p - 2)

    # Calculate the corresponding public key y
    y = pow(alpha, x, p)

    return {
        'p': p,  # modulus
        'alpha': alpha,  # generator
        'x': x,  # private key
        'y': y  # public key
    }


def encode(plaintext):
    plaintext_bytes = plaintext.encode('utf-8')
    return int.from_bytes(plaintext_bytes, 'big')


def decode(decrypted_int):
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
    return decrypted_bytes.decode('utf-8')


def encrypt(plaintext, public_key):
    p = public_key['p']
    alpha = public_key['alpha']
    y = public_key['y']

    # Convert plaintext to an element of the group
    m = encode(plaintext) % p

    # Choose a random k value
    k = random.randint(1, p - 2)

    # Calculate the ciphertext pair (c1, c2)
    c1 = pow(alpha, k, p)
    c2 = (m * pow(y, k, p)) % p

    return c1, c2


def decrypt(ciphertext, private_key):
    p = private_key['p']
    x = private_key['x']

    # Extract the ciphertext pair (c1, c2)
    c1, c2 = ciphertext

    # Calculate the shared secret s = c1^x mod p
    s = pow(c1, x, p)

    # Calculate the plaintext m = c2 / (s^k) mod p
    k_inv = pow(s, p-2, p)
    m = (c2 * k_inv) % p

    # Convert the plaintext back to its original form
    decrypted_int = m

    return decode(decrypted_int)


def decrypt2(ciphertext, private_key):
    p = private_key['p']
    x = private_key['x']

    # Extract the ciphertext pair (c1, c2)
    c1, c2 = ciphertext

    # Calculate the shared secret s = c1^x mod p
    s = fast_power(c1, x, p)

    # Calculate the plaintext m = c2 / (s^k) mod p
    k_inv = pow(s, p-2, p)
    m = (c2 * k_inv) % p

    # Convert the plaintext back to its original form
    decrypted_int = m

    return decode(decrypted_int)


def fast_power(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent // 2
        base = (base * base) % mod
    return result


if __name__ == '__main__':
    message = "Hello world abbcdefghijkklmnopqrstuvwxyz"
    key = generate_update()
    ciphertext = encrypt(message, key)
    print("ciphertext = " + str(ciphertext))
    start_time = time.time()
    plaintext = decrypt2(ciphertext, key)
    print("plaintext = " + plaintext)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.3f} seconds")
    print("ciphertext = " + str(ciphertext))
    plaintext2 = decrypt(ciphertext, key)
    print("plaintext2 = " + plaintext2)
    end_time2 = time.time()
    print(f"Time taken: {end_time2 - end_time:.3f} seconds")


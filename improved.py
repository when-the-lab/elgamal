import random
import math
import time
import Large_Prime_Generation
import gmpy2

# 生成密钥
def generate_keys(p):
    # 随机选择一个数作为私钥x
    x = random.randint(2, p-2)
    # 计算公钥y
    y = pow(g, x, p)
    # 返回公钥和私钥
    return (y, x)
def str_to_int(string):
    return int.from_bytes(string.encode('utf-8'), 'big')

# 将整数解码为字符串
def int_to_str(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode('utf-8')

# 加密
def encrypt(p, g, y, plaintext):
    plaintext_int = str_to_int(plaintext)
    # 随机选择一个数作为加密因子k
    k = random.randint(2, p-2)
    # 计算密文
    a = pow(g, k, p)
    b = (plaintext_int * pow(y, k, p)) % p
    # 返回密文
    return (a, b)

# 解密
def decrypt(p, x, ciphertext):
    a, b = ciphertext
    # 计算明文
    plaintext_int = (b * pow(a, p-1-x, p)) % p
    # 返回明文
    plaintext = int_to_str(plaintext_int)
    return plaintext



# 优化2：选择范围为[1, p-2]的随机数
def secure_random():
    return random.randint(1, p-2)


# 优化4：使用扩展欧几里得算法加速私钥生成
def generate_keys_fast(p):
    # 选择一个随机数k
    k = secure_random()
    # 使用扩展欧几里得算法计算私钥x和模反元素inv_k
    d, x, inv_k = extended_euclidean_algorithm(k, p-1)
    # 计算公钥y
    y = pow(g, x, p)
    # 返回公钥和私钥
    return (y, x)

# 扩展欧几里得算法
def extended_euclidean_algorithm(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = extended_euclidean_algorithm(b, a % b)
        return (d, y, x - (a // b) * y)

# 快速幂
def fast_power(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


# 加密
def encryptfast(p, g, y, plaintext):
    plaintext_int = str_to_int(plaintext)
    # 随机选择一个数作为加密因子k
    k = secure_random()
    # 计算密文
    a = pow(g, k, p)
    b = (plaintext_int * pow(y, k, p)) % p
    # 返回密文
    return (a, b)


# 解密
def decryptfast(p, x, ciphertext):
    a, b = ciphertext
    # 计算明文
    inv_a = fast_power(a, p-1-x, p)
    plaintext_int = (b * inv_a) % p
    # 返回明文
    plaintext = int_to_str(plaintext_int)
    return plaintext


# 选择范围为[1, p-2]的随机数
def secure_random():
    return random.randint(1, p-2)







if __name__ == '__main__':
    # 选择一个大素数作为模数p和一个原根g
    # 优化1：使用更大的p值
    p = Large_Prime_Generation.generate_prime()
    g = 2
# 测试
plaintext = "Helloworldsss"

start_time = time.time()
# 基本的ElGamal加密方案
public_key, private_key = generate_keys(p)
ciphertext = encrypt(p, g, public_key, plaintext)
decrypted_plaintext = decrypt(p, private_key, ciphertext)
print('基本的ElGamal加密方案：')
print('明文：', plaintext)
print('密文：', ciphertext)
print('解密后的明文：', decrypted_plaintext)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.3f} seconds")

# 基本的ElGamal升级加密方案
public_key, private_key = generate_keys_fast(p)
ciphertext = encrypt(p, g, public_key, plaintext)
decrypted_plaintext = decrypt(p, private_key, ciphertext)
print('基本的ElGamal extgcd加密方案：')
print('明文：', plaintext)
print('密文：', ciphertext)
print('解密后的明文：', decrypted_plaintext)
end_time2 = time.time()
print(f"Time taken: {end_time2 - end_time:.3f} seconds")


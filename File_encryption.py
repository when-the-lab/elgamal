import hashlib
import pickle
import random
import math
import time
import Large_Prime_Generation




def str_to_int(string):
    return int.from_bytes(string.encode('utf-8'), 'big')


# 将整数解码为字符串
def int_to_str(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode('utf-8')


def bytes_to_int(byte):
    return int.from_bytes(byte, 'big')


def int_to_bytes(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big')


# 加密
def encrypt(p, g, y, plaintext):
    plaintext_int = bytes_to_int(plaintext)
    # 随机选择一个数作为加密因子k
    k = random.randint(2, p - 2)
    # 计算密文
    a = pow(g, k, p)
    b = (plaintext_int * pow(y, k, p)) % p
    # 返回密文
    return (a, b)


# 解密
def decrypt(p, x, ciphertext):
    a, b = ciphertext
    # 计算明文
    plaintext_int = (b * pow(a, p - 1 - x, p)) % p
    # 返回明文
    plaintext = int_to_bytes(plaintext_int)
    return plaintext


# 优化2：选择范围为[1, p-2]的随机数
def secure_random(p):
    return random.randint(1, p - 2)


# 优化4：使用扩展欧几里得算法加速私钥生成
def generate_keys_fast(p, g):
    # 选择一个随机数k
    k = secure_random(p)
    # 使用扩展欧几里得算法计算私钥x和模反元素inv_k
    d, x, inv_k = extended_euclidean_algorithm(k, p - 1)
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
    plaintext_int = bytes_to_int(plaintext)
    # 随机选择一个数作为加密因子k
    k = secure_random(p)
    # 计算密文
    a = pow(g, k, p)
    b = (plaintext_int * pow(y, k, p)) % p
    # 返回密文
    return (a, b)


# 解密
def decryptfast(p, x, ciphertext):
    a, b = ciphertext
    # 计算明文
    inv_a = fast_power(a, p - 1 - x, p)
    plaintext_int = (b * inv_a) % p
    # 返回明文
    plaintext = int_to_bytes(plaintext_int)
    return plaintext


# 选择范围为[1, p-2]的随机数
def secure_random(p):
    return random.randint(1, p - 2)




def file_encrypt(file, p, g, public_key):
    start_time = time.time()
    with open(file, 'rb') as f:
        plain_text = f.read()
    cipher_text = [file]
    length = 64
    # print(plain_text)

    for i in range(0, len(plain_text), length):
        # print(plain_text[i:i + length])
        cipher_text.append(encryptfast(p, g, public_key, b'%'+plain_text[i:i + length]))
    new_path = file.rsplit(".", 1)[0] + "_encrypted" + "." + file.rsplit(".", 1)[1]
    # print(cipher_text)
    with open(new_path, 'wb') as f:
        pickle.dump(cipher_text, f)
    end_time = time.time()
    print("encrypted")
    print(f"Time taken: {end_time - start_time:.3f} seconds")


def file_decrypt(file, p, private_key):
    f = open(file, "rb")
    ciphered_text = pickle.load(f)
    # print(ciphered_text)
    path = ciphered_text[0]
    new_path = path.rsplit(".", 1)[0] + "_decrypted" + "." + path.rsplit(".", 1)[1]
    start_time = time.time()
    plain_text = b''
    for item in ciphered_text[1:]:
        plain_text += decryptfast(p, private_key, item)[1:]
    # print(plain_text)
    with open(new_path, "wb") as f:
        f.write(plain_text)
    end_time = time.time()
    print("decrypted")
    print(f"Time taken: {end_time - start_time:.3f} seconds")


def en_and_de(file):
    p = Large_Prime_Generation.generate_prime()
    g = 2
    public_key, private_key = generate_keys_fast(p, g)
    new_path = file.rsplit(".", 1)[0] + "_encrypted" + "." + file.rsplit(".", 1)[1]
    file_encrypt(file, p, g, public_key)
    file_decrypt(new_path, p, private_key)
    res_path = file.rsplit(".", 1)[0] + "_decrypted" + "." + file.rsplit(".", 1)[1]
    with open(file, 'rb') as fp:
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest()
    with open(res_path, 'rb') as new_fp:
        new_data = new_fp.read()
    new_file_md5 = hashlib.md5(new_data).hexdigest()
    # print(file_md5)
    # print(new_file_md5)
    if file_md5 == new_file_md5:
        print("success")
    else:
        print("fail")


if __name__ == '__main__':
    #输入文件地址
    file = "1.txt"
    en_and_de(file)






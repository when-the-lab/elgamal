import random
import math
import time
import Large_Prime_Generation
import gmpy2

import functools

import queue
import threading
import io
import os

from DebugTimer import DebugTimer

class QueueThread(threading.Thread):
    """A simple class to support tasks for queue in thread.

    Attributes:
        func: A function for the target task.
        queue: A queue.Queue object to acquire params for the function.
    """
    def __init__(self, func, queue):
        super().__init__()
        self.func = func
        self.queue = queue
        self.daemon = True

    def run(self):
        """Start function.
        """
        while True:
            # Exit the thread if there is no item in the queue.
            try:
                self.func(**self.queue.get_nowait())
            except queue.Empty:
                return
            self.queue.task_done()

block_size = 64
bytes_size = 129

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
def encryptfast(p, y, k, plaintext, idx, ciphertext: io.BytesIO):
    plaintext_int = str_to_int(plaintext[idx*block_size: idx*block_size+block_size])
    # 随机选择一个数作为加密因子k
    # 计算密文
    b = (plaintext_int * pow(y, k, p)) % p
    # 返回密文
    ciphertext.seek(idx * bytes_size, io.SEEK_SET)
    ciphertext.write(b.to_bytes(bytes_size, "big"))


# 解密
def decryptfast(p, x, a, idx, ciphertext: io.BytesIO, decrypt_text: io.StringIO):
    ciphertext.seek(idx*bytes_size, io.SEEK_SET)
    b = int.from_bytes(ciphertext.read(bytes_size), "big")
    # 计算明文
    plaintext_int = (b * pow(a, p-1-x, p)) % p
    # 返回明文

    plaintext = int_to_str(plaintext_int)
    decrypt_text.seek(idx * block_size, io.SEEK_SET)
    decrypt_text.write(plaintext)



# 选择范围为[1, p-2]的随机数
def secure_random():
    return random.randint(1, p-2)




if __name__ == '__main__':
    # 选择一个大素数作为模数p和一个原根g
    # 优化1：使用更大的p值
    p = Large_Prime_Generation.generate_prime()
    g = 2
# 测试
  #./1.txt
    with open("./1.txt", "r") as fp:
        plaintext = fp.read()
    print(len(plaintext), plaintext[: 10])

    public_key, private_key = generate_keys(p)



    crypt_queue = queue.Queue()

    k = secure_random()
    a = pow(g, k, p)

    ciphertext = io.BytesIO()

    with DebugTimer("Encryption"):
        for idx in range(math.ceil(len(plaintext)/block_size)):
            crypt_queue.put({
                "idx": idx,
            })
        for _ in range(10):
            QueueThread(functools.partial(
                encryptfast,
                p=p,
                y=public_key,
                k=k,
                plaintext=plaintext,
                ciphertext=ciphertext
            ), crypt_queue).start()
        crypt_queue.join()

    decrypt_queue = queue.Queue()
    decrypt_text = io.StringIO()

    with DebugTimer("Decryption"):
        for idx in range(math.ceil(len(plaintext)/block_size)):
            decrypt_queue.put({
                "idx": idx,
            })
        for _ in range(16):
            QueueThread(functools.partial(
                decryptfast,
                p=p,
                a=a,
                x=private_key,
                ciphertext=ciphertext,
                decrypt_text=decrypt_text
            ), decrypt_queue).start()
        decrypt_queue.join()

    print(len(decrypt_text.getvalue()), decrypt_text.getvalue()[: 10])
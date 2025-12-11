import random
import math
import time
# 生成密钥
import Large_Prime_Generation
def str_to_int(string):
    return int.from_bytes(string.encode('utf-8'), 'big')

# 将整数解码为字符串
def int_to_str(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode('utf-8')


def generate_keys(p):
    # 随机选择一个数作为私钥x
    x = random.randint(2, p-2)
    # 计算公钥y
    y = pow(g, x, p)
    # 返回公钥和私钥
    return (y, x)

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

if __name__ == '__main__':
    # 选择一个大素数作为模数p和一个原根g
    #p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    p = Large_Prime_Generation.generate_prime()
    g = 2

# 测试
plaintext = "Hello worldsss"
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
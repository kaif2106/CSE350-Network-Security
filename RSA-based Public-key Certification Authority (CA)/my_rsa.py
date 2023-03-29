import random
from math import gcd

def generate_keypair(p, q):
    n = p * q
    lambda_n = (p - 1) * (q - 1)
    e = random.randrange(1, lambda_n)
    g = gcd(e, lambda_n)
    while g != 1:
        e = random.randrange(1, lambda_n)
        g = gcd(e, lambda_n)
    d = inverse_mod(e, lambda_n)
    return ((n,e), (n,d))

def inverse_mod(a: int, m: int):
    if gcd(a,m) != 1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3 != 0:
        q = u3 // v3
        v1,v2,v3,u1,u2,u3 = (u1 - q*v1), (u2 - q*v2), (u3 - q*v3), v1,v2,v3
    return u1 % m

def encrypt(pk, plaintext):
    n,e = pk
    cipher = [pow(ord(char),e,n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    n,d = pk
    plain = [chr(pow(char,d,n)) for char in ciphertext]
    return ''.join(plain)

# if __name__ == '__main__':
#     p,q = 61,53
#     public_key,private_key = generate_keypair(p,q)
#     print("Public key is", public_key)
#     print("Private key is", private_key)
#     message = "Hello World"
#     encrypted_message = encrypt(public_key,message)
#     print("Encrypted message is", ''.join(map(str,encrypted_message)))
#     decrypted_message = decrypt(private_key,encrypted_message)
#     print("Decrypted message is", decrypted_message)
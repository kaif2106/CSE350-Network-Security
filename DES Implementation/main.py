# initial permutation
# round operation - swap, F box
# key generation
from helper import *
from subkey_gen import *

def bin2str(text):
    byte = [text[i:i+8] for i in range(0, len(text), 8)]
    string = ""
    for i in byte:
      string+=chr(int(i, 2))

    return string

def str2bin(data):
    data = bytes(data, 'utf-8')
    return ''.join(format(byte, '08b') for byte in data)
  
def encrypt(binary_data, subkeys):
    # Perform initial permutation on input data
    binary_data_permuted = ""
    for i in range(64):
        binary_data_permuted+=binary_data[initial_permutation[i]-1]

    # Perform 16 rounds of encryption
    for i in range(16):
        # Divide the 64-bit input into two 32-bit halves
        left_half, right_half = binary_data_permuted[:32], binary_data_permuted[32:]
        # Perform expansion and permutation on the right half
        expanded_right = expand_permutation(right_half)
        # XOR the expanded right half with the current subkey
        subkey = subkeys[i]
        xor_result = xor(expanded_right, subkey)
        # Perform substitution using S-boxes
        sbox_result = sbox_substitution(xor_result)
        # Perform permutation using a fixed permutation table
        permuted_result=""
        for j in range(32):
            permuted_result+=sbox_result[p_table[j]-1]
        # XOR the left half with the permuted result
        xor_result = xor(left_half, permuted_result)
        # Combine the left and right halves and swap them
        if i==15:
            binary_data_permuted = xor_result + right_half
        else:
            binary_data_permuted = right_half + xor_result

    # Perform final permutation on the output data
    cipher = ""
    for i in range(64):
        cipher+=binary_data_permuted[final_perm[i]-1]
    return cipher

def decrypt(cipher, subkeys):
    rev_keys = subkeys[::-1]
    data = encrypt(cipher, rev_keys)
    return data

if __name__ =='__main__':
    # byte object
    data = "qwertyui"
    key = "eightbit"

    binary_data = str2bin(data)
    binary_key = str2bin(key)

    print(binary_data)
    subkeys = generate_subkeys(binary_key)
    cipher = encrypt(binary_data, subkeys)
    # print("Cipher: " + cipher)
    
    decrypted_text = decrypt(cipher, subkeys)
    print(decrypted_text)
    decrypted_str = bin2str(decrypted_text)
    print(decrypted_str)
# initial permutation
# round operation - swap, F box
# key generation

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64



def generate_subkeys(key):
    # Perform PC-1 permutation/parity drop on 64-bit key
    pc1_table = [57, 49, 41, 33, 25, 17, 9,
                 1, 58, 50, 42, 34, 26, 18,
                 10, 2, 59, 51, 43, 35, 27,
                 19, 11, 3, 60, 52, 44, 36,
                 63, 55, 47, 39, 31, 23, 15,
                 7, 62, 54, 46, 38, 30, 22,
                 14, 6, 61, 53, 45, 37, 29,
                 21, 13, 5, 28, 20, 12, 4]
    pc1_result=""
    for i in range(56):
        pc1_result+=key[pc1_table[i]-1]
    
    # Split the 56-bit key into two 28-bit halves
    l_half, r_half = pc1_result[:28], pc1_result[28:]
    
    # Generate 16 subkeys using the key schedule algorithm
    subkeys = []

    # Left shift by 1 in round 1,2,9,16
    # Left shift by two otherwise
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    #Compression P-box
    pc2_table = [14, 17, 11, 24, 1, 5, 3, 28,
                 15, 6, 21, 10, 23, 19, 12, 4,
                 26, 8, 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55, 30, 40,
                 51, 45, 33, 48, 44, 49, 39, 56,
                 34, 53, 46, 42, 50, 36, 29, 32]
    subkeys = []
    for i in range(16):
        # Left shifting the 2 halves
        l_half = l_half[shift_table[i]:] + l_half[:shift_table[i]]
        r_half = r_half[shift_table[i]:] + r_half[:shift_table[i]]
        # Combine the halves and perform PC-2 permutation
        combined_half = l_half + r_half
        pc2_result = ""
        for j in range(48):
            pc2_result += combined_half[pc2_table[j]-1]
        subkeys.append(pc2_result)
    return subkeys

def expand_permutation(right_half):
    exp_d = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    expanded_right = ""
    for i in range(48):
        expanded_right += right_half[exp_d[i]-1]
    return expanded_right

def xor(op1, op2):
    ans = ""
    length = len(op1)
    for i in range(length):
        ans+=str(int(op1[i]) ^ int(op2[i]))
    return ans

def sbox_substitution(inp):
    s = [
        [ 14, 4,  13, 1, 2,  15, 11, 8,  3,  10, 6,  12, 5,
          9,  0,  7,  0, 15, 7,  4,  14, 2,  13, 1,  10, 6,
          12, 11, 9,  5, 3,  8,  4,  1,  14, 8,  13, 6,  2,
          11, 15, 12, 9, 7,  3,  10, 5,  0,  15, 12, 8,  2,
          4,  9,  1,  7, 5,  11, 3,  14, 10, 0,  6,  13 ],
        [ 15, 1,  8,  14, 6,  11, 3, 4,  9,  7,  2,  13, 12,
          0,  5,  10, 3,  13, 4,  7, 15, 2,  8,  14, 12, 0,
          1,  10, 6,  9,  11, 5,  0, 14, 7,  11, 10, 4,  13,
          1,  5,  8,  12, 6,  9,  3, 2,  15, 13, 8,  10, 1,
          3,  15, 4,  2,  11, 6,  7, 12, 0,  5,  14, 9 ],
 
        [ 10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12,
          7,  11, 4,  2,  8,  13, 7,  0,  9,  3,  4,
          6,  10, 2,  8,  5,  14, 12, 11, 15, 1,  13,
          6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12,
          5,  10, 14, 7,  1,  10, 13, 0,  6,  9,  8,
          7,  4,  15, 14, 3,  11, 5,  2,  12 ],
        [ 7,  13, 14, 3,  0,  6,  9,  10, 1,  2, 8,  5,  11,
          12, 4,  15, 13, 8,  11, 5,  6,  15, 0, 3,  4,  7,
          2,  12, 1,  10, 14, 9,  10, 6,  9,  0, 12, 11, 7,
          13, 15, 1,  3,  14, 5,  2,  8,  4,  3, 15, 0,  6,
          10, 1,  13, 8,  9,  4,  5,  11, 12, 7, 2,  14 ],
        [ 2,  12, 4, 1,  7,  10, 11, 6, 8,  5,  3,  15, 13,
          0,  14, 9, 14, 11, 2,  12, 4, 7,  13, 1,  5,  0,
          15, 10, 3, 9,  8,  6,  4,  2, 1,  11, 10, 13, 7,
          8,  15, 9, 12, 5,  6,  3,  0, 14, 11, 8,  12, 7,
          1,  14, 2, 13, 6,  15, 0,  9, 10, 4,  5,  3 ],
        [ 12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3, 4, 14,
          7,  5,  11, 10, 15, 4,  2,  7,  12, 9,  5, 6, 1,
          13, 14, 0,  11, 3,  8,  9,  14, 15, 5,  2, 8, 12,
          3,  7,  0,  4,  10, 1,  13, 11, 6,  4,  3, 2, 12,
          9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8, 13 ],
        [ 4,  11, 2,  14, 15, 0,  8, 13, 3,  12, 9,  7,  5,
          10, 6,  1,  13, 0,  11, 7, 4,  9,  1,  10, 14, 3,
          5,  12, 2,  15, 8,  6,  1, 4,  11, 13, 12, 3,  7,
          14, 10, 15, 6,  8,  0,  5, 9,  2,  6,  11, 13, 8,
          1,  4,  10, 7,  9,  5,  0, 15, 14, 2,  3,  12 ],
        [ 13, 2,  8, 4,  6,  15, 11, 1,  10, 9, 3, 14, 5,
          0,  12, 7, 1,  15, 13, 8,  10, 3,  7, 4, 12, 5,
          6,  11, 0, 14, 9,  2,  7,  11, 4,  1, 9, 12, 14,
          2,  0,  6, 10, 13, 15, 3,  5,  8,  2, 1, 14, 7,
          4,  10, 8, 13, 15, 12, 9,  0,  3,  5, 6, 11 ]
    ]
    binary_list = [inp[i:i+6] for i in range(0, len(inp), 6)]
    result = ""
    c = 0
    for i in binary_list:
        row = int(i[1:5], 2)
        col = int(i[0]+i[5], 2)
        ind = (col*15)+row
        result+='{0:04b}'.format(s[c][ind])
        c+=1
    return result


if __name__ =='__main__':
    # byte object
    data = b"qwertyui"
    key = b"eightbit"

    binary_data = ''.join(format(byte, '08b') for byte in data)
    binary_key = ''.join(format(byte, '08b') for byte in key)

    # print(binary_key)
    # print(len(binary_key))
    # print(chr(int("01100101", 2)))


    # Perform initial permutation on input data
    ip_table = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

    binary_data_permuted = ""
    for i in range(64):
        binary_data_permuted+=binary_data[ip_table[i]-1]
    # print(binary_data)
    # print(binary_data_permuted)

    # Generate 16 48-bit subkeys using the key schedule algorithm
    subkeys = generate_subkeys(binary_key)
    # for subkey in subkeys:
    #     print(subkey)
    #     print(len(subkey))
    # exit()

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
        # print(sbox_result)
        # print(len(sbox_result))
        # Perform permutation using a fixed permutation table
        p_table = [16, 7, 20, 21, 29, 12, 28, 17,
                1, 15, 23, 26, 5, 18, 31, 10,
                2, 8, 24, 14, 32, 27, 3, 9,
                19, 13, 30, 6, 22, 11, 4, 25]
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
        # print(binary_data_permuted)
        # print(len(binary_data_permuted))
        #if i != 15:
        #    binary_data_permuted, right_half = right_half, binary_data_permuted


    # Perform final permutation on the output data
    final_perm = [ 40, 8,  48, 16, 56, 24, 64, 32, 39, 7,  47,
            15, 55, 23, 63, 31, 38, 6,  46, 14, 54, 22,
            62, 30, 37, 5,  45, 13, 53, 21, 61, 29, 36,
            4,  44, 12, 52, 20, 60, 28, 35, 3,  43, 11,
            51, 19, 59, 27, 34, 2,  42, 10, 50, 18, 58,
            26, 33, 1,  41, 9,  49, 17, 57, 25 ]
    cipher = ""
    for i in range(64):
        cipher+=binary_data_permuted[final_perm[i]-1]
    print(len(cipher))
    print(cipher)
    

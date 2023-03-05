# initial permutation
# round operation - swap, F box
# key generation

def generate_subkeys(key):
    # Perform PC-1 permutation/parity drop on 64-bit key
    print(key)
    pc1_table = [57, 49, 41, 33, 25, 17, 9,
                 1, 58, 50, 42, 34, 26, 18,
                 10, 2, 59, 51, 43, 35, 27,
                 19, 11, 3, 60, 52, 44, 36,
                 63, 55, 47, 39, 31, 23, 15,
                 7, 62, 54, 46, 38, 30, 22,
                 14, 6, 61, 53, 45, 37, 29,
                 21, 13, 5, 28, 20, 12, 4]
    pc1_result = [key[pc1_table[i]-1] for i in range(56)]
    
    # Split the 56-bit key into two 28-bit halves
    c_half, d_half = pc1_result[:28], pc1_result[28:]
    
    # Generate 16 subkeys using the key schedule algorithm
    subkeys = []

    # Left shift by 1 in round 1,2,9,16
    # Left shift by two otherwise
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    #Compression D-box
    pc2_table = [14, 17, 11, 24, 1, 5, 3, 28,
                 15, 6, 21, 10, 23, 19, 12, 4,
                 26, 8, 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55, 30, 40,
                 51, 45, 33, 48, 44, 49, 39, 56,
                 34, 53, 46, 42, 50, 36, 29, 32]
    for i in range(16):
        # Left shifting the 2 halves
        c_half = c_half[shift_table[i]:] + c_half[:shift_table[i]]
        d_half = d_half[shift_table[i]:] + d_half[:shift_table[i]]
        # Combine the halves and perform PC-2 permutation
        combined_half = c_half + d_half
        pc2_result = [combined_half[pc2_table[i]-1] for i in range(48)]
        subkeys.append(''.join(pc2_result))
    return subkeys


if __name__ =='__main__':
    # byte object
    data = b"Hello world"
    key = b"my secret key"

    binary_data = ''.join(format(byte, '08b') for byte in data)
    binary_key = ''.join(format(byte, '08b') for byte in key)

    # Perform initial permutation on input data
    ip_table = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

    binary_data_permuted = [binary_data[ip_table[i]-1] for i in range(64)]

    # Generate 16 48-bit subkeys using the key schedule algorithm
    subkeys = generate_subkeys(binary_key)
    print(subkeys)
    exit()

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
        p_table = [16, 7, 20, 21, 29, 12, 28, 17,
                1, 15, 23, 26, 5, 18, 31, 10,
                2, 8, 24, 14, 32, 27, 3, 9,
                19, 13, 30, 6, 22, 11, 4, 25]
        permuted_result = [sbox_result[p_table[i]-1] for i in range(32)]
        # XOR the left half with the permuted result
        xor_result = xor(left_half, permuted_result)
        # Combine the left and right halves and swap them
        binary_data_permuted = right_half + xor_result
        if i != 15:
            binary_data_permuted, right_half = right_half, binary_data_permuted

    # Perform final permutation on the output data
    fp_table = [40, 8, 48, 16]

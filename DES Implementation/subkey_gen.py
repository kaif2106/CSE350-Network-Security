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
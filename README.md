Assignments done in the course CSE350-Network Security

Block size = 64 bits
Key size = 56 (64 - Parity bits [8th bits])
Rounds = 16

Round Process:
    1) Key Transformation (Selecting 48bit key from 56bit key)
    2) Expansion permutation
    3) XOR with key
    4) S-box permutation
    5) P-box permutation
    6) XOR with other side (Swap)
    
![image](https://user-images.githubusercontent.com/29958259/223635697-fb71392b-35ac-474b-9749-cad9edbf7d2a.png)

Key Transformation:

![image](https://user-images.githubusercontent.com/29958259/223636056-ca0b8226-c3fe-4a59-b3a4-ee34b3ddce92.png)

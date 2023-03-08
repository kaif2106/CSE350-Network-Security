## DES

**Block size** = 64 bits<br>
**Key size** = 56 (64 - Parity bits [8th bits])<br>
**Rounds** = 16<br>

### Round Process
- Key Transformation (Selecting 48bit key from 56bit key)
- Expansion permutation
- XOR with key
- S-box permutation
- P-box permutation
- XOR with other side (Swap)
    
![image](https://user-images.githubusercontent.com/29958259/223635697-fb71392b-35ac-474b-9749-cad9edbf7d2a.png)

![image](https://user-images.githubusercontent.com/29958259/223639552-f943ff9b-74c2-468e-bd6c-9daaa7b89dcf.png)

### Key Transformation:

![image](https://user-images.githubusercontent.com/29958259/223636056-ca0b8226-c3fe-4a59-b3a4-ee34b3ddce92.png)

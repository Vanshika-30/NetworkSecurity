'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import random
from Crypto.Util.number import getPrime

def generate_key():
    key = ""
    for _ in range(8):
        p = random.randint(0,9)
        key += str(p)
    return key

if __name__ == "__main__":
    R = random.randint(1,1000000000)
    Key_A = generate_key()
    R_A = getPrime(10)

    f = open("BT18CSE107_A_KDC.txt", 'w')
    f.write(Key_A + " " + str(R_A) + " " + str(R))
    f.close()

    Key_B = generate_key()
    while (Key_A == Key_B):
        Key_B = generate_key()
    
    R_B = getPrime(10)
    while (R_A == R_B):
        R_B = getPrime(10)

    f = open("BT18CSE107_B_KDC.txt", 'w')
    f.write(Key_B + " " + str(R_B) + " " + str(R))
    f.close()
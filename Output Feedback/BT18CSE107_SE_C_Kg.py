'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''
import random

BLOCKSIZE = 8

def generate_key():
    key = ""
    for _ in range(8):
        p = random.randint(0,9)
        key += str(p)
    return key

if __name__ == "__main__":
    f = open('BT18CSE107_key.txt','wb')
    key = bytearray(generate_key(), "utf-8")
    f.write(key)
    f.close()

    f = open('BT18CSE107_iv.txt','wb')
    iv = bytearray(generate_key(), "utf-8")
    f.write(iv)
    f.close()
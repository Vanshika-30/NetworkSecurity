'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket, random
from Crypto.Util.number import getPrime
from Crypto.Cipher import DES
from sys import argv

BLOCKSIZE = 8

def generate_key():
    key = ""
    for _ in range(8):
        p = random.randint(0,9)
        key += str(p)
    return key

def get_blocks(message):
    global BLOCKSIZE
    msg_len = len(message)
    if msg_len % BLOCKSIZE == 0:
        padded_PT = message
    else:
        padded_PT = message + bytearray(0 for i in range(BLOCKSIZE - msg_len % BLOCKSIZE))
    des_PT = []
    for i in range(0, len(padded_PT), BLOCKSIZE):
        des_PT.append(padded_PT[i : i + BLOCKSIZE])
    
    return des_PT

def encrypt(text,key):
    blocks = get_blocks(text)
    result = []
    for block in blocks:
        des = DES.new(key, DES.MODE_ECB)
        enc_out = des.encrypt(block)
        result += enc_out
    return bytes(result)

def decrypt(text,key):
    blocks = get_blocks(text)
    result = []
    for block in blocks:
        des = DES.new(key, DES.MODE_ECB)
        enc_out = des.decrypt(block)
        result += enc_out
    return bytes(result)


if __name__ == '__main__':
    # Create a socket object
    socket_KDC = socket.socket()        
    
    # Define the port on which you want to connect
    port_KDC = 12345
    host_KDC = 'localhost'

    keys = ["--hostK=","--portK=","-hk=","-pk=", "--key_size=", "-ks"]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--hostA=' or key == '-ha=':
                    host_KDC = argv[i][len(key):]
                elif key == '--portA=' or key == '-pa=':
                    port_KDC = int(argv[i][len(key):]) 
                elif key == '--key_size=' or key == '-ks=':
                    N = int(argv[i][len(key):])             
    
    # connect to the server on local computer
    socket_KDC.connect((host_KDC, port_KDC))
    print("Connected to host: ", host_KDC)    

    # KDC reading his secret key with alice, random nonce with Alice and common nonce
    f = open("BT18CSE107_A_KDC.txt", 'r')
    lines = f.readline()
    Key_A, R_A, R1 = lines.split(" ")
    Key_A, R_A, R1 = bytearray(Key_A, "utf-8"), bytes(R_A, "utf-8"), bytearray(R1, "utf-8")
    f.close()

    # KDC reading his secret key with Bob, random nonce with Bob and common nonce
    f = open("BT18CSE107_B_KDC.txt", 'r')
    lines = f.readline()
    Key_B, R_B, R2 = lines.split(" ")
    Key_B, R_B, R2 = bytearray(Key_B, "utf-8"), bytes(R_B, "utf-8"), bytearray(R2, "utf-8")
    f.close()

    if R1 == R2:
        R = R2

    enc_text_kdc = socket_KDC.recv(1024)
    text_A, text_B = enc_text_kdc.split(b',')

    decrypt_A = decrypt(text_A, Key_A)
    decrypt_B = decrypt(text_B, Key_B)

    A1, B1, R1, R_A1 = decrypt_A.split(b',')

    A2, B2, R2, R_B1 = decrypt_B.split(b',')

    if get_blocks(R_A) != get_blocks(R_A1) and get_blocks(R_B) != get_blocks(R_B1): 
        print("Fake person!!")
        socket_KDC.send(bytearray("error", "utf-8"))
        socket_KDC.close()
        exit(0)

    sk = bytearray(generate_key(), "utf-8")
    print("\nSession Key Generated: ", sk)
    
    sk_text = R + bytearray(",", "utf-8")  + encrypt(R_B + bytearray(",", "utf-8") + sk, Key_B) + bytearray(",", "utf-8")  + encrypt(R_A + bytearray(",", "utf-8") + sk, Key_A)
        
    socket_KDC.send(sk_text)

    socket_KDC.close()
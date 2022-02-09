'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket
import time
from Crypto.Cipher import DES
from sys import argv

PT_BLOCKSIZE = 4
IV_SIZE = 8

def XOR(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def get_blocks(message):
    msg_len = len(message)
    if msg_len % PT_BLOCKSIZE == 0:
        padded_PT = message
    else:
        padded_PT = message + bytearray(0 for _ in range(PT_BLOCKSIZE - msg_len % PT_BLOCKSIZE))
    des_PT = []
    for i in range(0, len(padded_PT), PT_BLOCKSIZE):
        des_PT.append(padded_PT[i : i + PT_BLOCKSIZE])
    
    return des_PT

def shift_left(shift_input, feedback):
    temp = shift_input[IV_SIZE - PT_BLOCKSIZE:]
    return (temp + feedback)

def encrypt(message_bytes, key, IV):
    PT_blocks = get_blocks(message_bytes)
    shift_input = IV
    cipher_text = []
    count = 1
    print("\n\n------- Encryption Process -------")

    for block in PT_blocks:
        print("Plain Text Block: ", block)
        
        if count == 1:
            shift_input = IV
        else:
            shift_input = shift_left(shift_input, feedback)
            
        des = DES.new(key, DES.MODE_ECB)
        enc_out = des.encrypt(shift_input)
        feedback = enc_out[:PT_BLOCKSIZE]
        temp_c = XOR(block, enc_out[:PT_BLOCKSIZE])
        cipher_text += temp_c
        count += 1
    
    return bytes(cipher_text), PT_blocks

if __name__ == "__main__":
    
    sock = socket.socket()        
    print ("Socket successfully created")
    port = 12345               
    host = 'localhost'
    
    keys = ["--host=","--port=","-h=","-p="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--host=' or key == '-h=':
                    host = argv[i][len(key):]
                elif key == '--port=' or key == '-p=':
                    port = int(argv[i][len(key):])

    sock.bind((host, port))         
    print ("socket binded to %s" %(port))
    
    sock.listen(5)    
    print ("socket is listening")           
  
    conn, addr = sock.accept()    
    print ('Got connection from', addr )

    f =  open("BT18CSE107_key.txt", 'rb')
    key = f.readline()
    f.close()

    f =  open("BT18CSE107_iv.txt", 'rb')
    IV = f.readline()
    f.close()

    f = open('../input.txt', 'r')
    for line in f.readlines():
        PT = line.strip()

        PT_bytes = PT.encode("utf-8")
        cipher_text, padded_PT = encrypt(PT_bytes, key, IV)
        conn.send(cipher_text)

        print("\n----- Final Output -----")
        print("Plain Text sent: ", PT)
        print("Encrypted Cipher Text:", cipher_text)
        
        if PT == "exit":
            print("\nClosing connection with ", host)
            conn.close()
            break

        time.sleep(0.25)

    f.close()





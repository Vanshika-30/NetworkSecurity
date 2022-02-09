'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket
from Crypto.Cipher import DES
from sys import argv 
from BT18CSE107_SE_C_En import PT_BLOCKSIZE, IV_SIZE, XOR

CT_BLOCKSIZE = PT_BLOCKSIZE

def get_blocks(message):
    msg_len = len(message)
    if msg_len % CT_BLOCKSIZE == 0:
        padded_PT = message
    else:
        padded_PT = message + bytearray(0 for i in range(CT_BLOCKSIZE - msg_len % CT_BLOCKSIZE))
    des_PT = []
    for i in range(0, len(padded_PT), CT_BLOCKSIZE):
        des_PT.append(padded_PT[i : i + CT_BLOCKSIZE])
    
    return des_PT

def shift_left(shift_input, feedback):
    temp = shift_input[IV_SIZE - CT_BLOCKSIZE:]
    return (temp + feedback)

def decrypt(message_bytes, key, IV):
    CT_blocks = get_blocks(message_bytes)
    shift_input = IV
    plain_text = []
    count = 1
    print("\n\n------- Decryption Process -------")
    for block in CT_blocks:
        print('Cipher Text Block: ', block)
        
        if count == 1:
            shift_input = IV
        else:
            shift_input = shift_left(shift_input, feedback)
            
        des = DES.new(key, DES.MODE_ECB)
        enc_out = des.encrypt(shift_input)
        feedback = enc_out[:CT_BLOCKSIZE]
        temp_p = XOR(block, feedback)
        plain_text += temp_p
        count += 1
    return bytes(plain_text), CT_blocks

if __name__ == "__main__":
    
    sock = socket.socket()        
    # Define the port on which you want to connect
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

    # connect to the server on local computer
    sock.connect((host, port))               
    print("Connected to host: ", host)    

    f =  open("BT18CSE107_key.txt", 'rb')
    key = f.readline()
    f.close()

    f =  open("BT18CSE107_iv.txt", 'rb')
    IV = f.readline()
    f.close()

    while True:
        cipher_text = sock.recv(2048)

        plain_text, padded_CT = decrypt(cipher_text, key, IV)

        print("\n----- Final Output -----")
        print("Cipher Text Received: ", cipher_text)
        print("Decrypted Plain Text:", plain_text.decode("ASCII"))
        
        if plain_text.decode("ASCII") == "exit":
            print("\nClosing connection with ", host)
            sock.close()
            break
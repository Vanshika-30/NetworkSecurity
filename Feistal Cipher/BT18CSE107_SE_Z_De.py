'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
    For executing: python keyGeneration.py size_of_key 
'''

import socket
from sys import argv
from BT18CSE107_SE_Z_En import round_func, XOR, revive_text

# helper function which perfeorms the decryption process
def feistal_decrypt(ct, rounds=2):
    n = len(ct)
    L = ct[0:n//2]
    R = ct[n//2:]
    
    keys = []
    f = open("BT18CSE107_keys.txt", 'r')
    for line in f.readlines():
        keys.append(line.strip())
    f.close()
    
    for i in range(rounds):
        key = keys[len(keys) - 1 - i]
        L_new = XOR(R, round_func(L, key))
        R_new = L

        L = L_new
        R = R_new

    return L_new + R_new


if __name__ == '__main__':
    # Create a socket object
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
    
    while True:
    # receive data from the server and decoding to get the string.
        input_string = sock.recv(2048).decode()

        if input_string == "exit":
            print("Closing connection with ", host)
            sock.close()
            break
        
        pt = feistal_decrypt(input_string)
        PT = revive_text(pt)
        CT = revive_text(input_string)
        
        print("\nCipher Text Decrypted: ", CT)
        print("Plain Text Received: " ,PT)
        
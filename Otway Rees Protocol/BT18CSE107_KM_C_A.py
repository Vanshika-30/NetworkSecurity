'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket, time
from Crypto.Cipher import DES
from sys import argv
from BT18CSE107_KM_C_Kdc import encrypt, decrypt

if __name__ == '__main__':
    # Create a socket object
    socket_Alice = socket.socket()        
    
    # Define the port on which you want to connect
    port_Alice = 12346  
    host_Alice = 'localhost'

    keys = ["--hostA=","--portA=","-ha=","-pa="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--hostA=' or key == '-ha=':
                    host_Alice = argv[i][len(key):]
                elif key == '--portA=' or key == '-pa=':
                    port_Alice = int(argv[i][len(key):])             
    
    # connect to the server on local computer
    socket_Alice.connect((host_Alice, port_Alice))
    print("Connected to host: ", host_Alice) 

    # Alice reading his secret key with KDC, random nonce with KDC and common nonce
    f = open("BT18CSE107_A_KDC.txt", 'r')
    lines = f.readline()
    Key_A, R_A, common_R = lines.split(" ")
    Key_A = bytearray(Key_A, "utf-8")
    f.close()

    enc_text = encrypt(bytearray("Alice,Bob," + common_R + "," + R_A , "utf-8"), Key_A)
    text = bytearray("Alice,Bob,"+ common_R + ",", "utf-8") + enc_text
    # print(text.split(b','))
    # exit(0)
    socket_Alice.send(text)

    input_string = socket_Alice.recv(1024)

    if input_string == b'error\x00\x00\x00':
        print("Fake person!!")
        socket_Alice.close()
        exit(0)

    RA_rec, sk = decrypt(input_string, Key_A).split(b',')

    sk = sk[:8]
    print("Secret Key Received: ", sk)

    f = open('../input.txt', 'r')
    for line in f.readlines(): 
        PT = line.strip()
        msg = encrypt(bytearray(PT, "utf-8"), sk)  
        socket_Alice.send(msg)
        print("Message Sent!")

        if PT == "exit":
            print("\nClosing connection with ", host_Alice)
            socket_Alice.close()
            break
        time.sleep(0.25)
    f.close()
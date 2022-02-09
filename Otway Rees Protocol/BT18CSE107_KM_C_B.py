'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket
from Crypto.Cipher import DES
from sys import argv
from BT18CSE107_KM_C_Kdc import encrypt, decrypt

if __name__ == '__main__':     
    socket_KDC = socket.socket()  
    socket_Alice = socket.socket()      
    print ("Socket successfully created")
     
    port_KDC = 12345   
    port_Alice = 12346               
    host_KDC = 'localhost'
    host_Alice = 'localhost'

    keys = ["--hostA=","--portA=","-ha=","-pa=", "--hostK=","--portK=","-hk=","-pk="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--hostA=' or key == '-ha=':
                    host_Alice = argv[i][len(key):]
                elif key == '--portA=' or key == '-pa=':
                    port_Alice = int(argv[i][len(key):])
                elif key == '--portK=' or key == '-pk=':
                    port_KDC = int(argv[i][len(key):])
                elif key == '--hostK=' or key == '-hk=':
                    host_KDC = int(argv[i][len(key):])
    
    socket_KDC.bind((host_KDC, port_KDC))        
    print ("socket 1 binded to %s" %(port_KDC))
    
    socket_Alice.bind((host_Alice, port_Alice))        
    print ("socket 2 binded to %s" %(port_Alice))
    
    socket_KDC.listen(5)    
    print ("socket 1 is listening")
    socket_Alice.listen(5)    
    print ("socket 2 is listening")           
  
    conn_KDC, addr_KDC = socket_KDC.accept()    
    print ('Got connection from', addr_KDC)

    conn_Alice, addr_Alice = socket_Alice.accept()    
    print ('Got connection from', addr_Alice)

    # Bob reading his secret key with KDC, random nonce with KDC and common nonce
    f = open("BT18CSE107_B_KDC.txt", 'r')
    lines = f.readline()
    Key_B, R_B, common_R = lines.split(" ")
    Key_B = bytearray(Key_B, "utf-8")
    f.close()

    input_string = conn_Alice.recv(2048)
    name1, name2, R_recv, enc_text_A = input_string.split(b',')

    enc_text_B = encrypt(bytearray("Alice,Bob," , "utf-8")+ R_recv + bytearray("," + R_B , "utf-8"), Key_B)
    
    kdc_text = enc_text_A + bytearray(",", "utf-8") + enc_text_B
    conn_KDC.send(kdc_text)

    input_string = conn_KDC.recv(1024)

    if input_string == b'error\x00\x00\x00':
        print("Fake person!!")
        conn_Alice.send(bytearray("error", "utf-8"))
        conn_KDC.close()
        conn_Alice.close()
        exit(0)

    R_rec, SK_B, SK_A = input_string.split(b',')
    
    if bytes(common_R, "utf-8") ==  R_rec:
        conn_Alice.send(SK_A)

        RB_rec, sk = decrypt(SK_B, Key_B).split(b',')

        sk = sk[:8]
        
        print("Secret Key Received: ", sk)

        conn_KDC.close()

        while True:
            msg_rec = conn_Alice.recv(1024)
            msg = decrypt(msg_rec, sk)

            print("Received Msg: ", msg.decode("utf-8"))
            
            if msg == b'exit\x00\x00\x00\x00':
                print("\nClosing connection with ", host_Alice)
                conn_Alice.close()
                break
            
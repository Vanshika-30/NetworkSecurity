'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
    For executing: python keyGeneration.py size_of_key 
'''

import socket, time
import random
from sys import argv

# Padding text to form B bit binary
def binary_padded(s, N=8):
    # converting text to ASCII then binary
    bnr = "{0:b}".format(ord(s))
    bnr = '0'*(N-len(bnr)) + bnr
    return bnr

# Genearte random binary key of size n
def generate_key(n):
    key1 = ""
    for _ in range(n):
        temp = str(random.randint(0, 1))
        key1 += temp
         
    return key1
 
# XOR helper function
def XOR(a,b):
    temp = ""
    n = len(a)
    for i in range(n):
        if (a[i] == b[i]):
            temp += "0"  
        else:
            temp += "1"   
    return temp

# Round function f 
def round_func(a, b, roll_no = "107"):
    # padding roll no.
    rn = binary_padded(roll_no[1], 4) + binary_padded(roll_no[2], 4)
    n = len(a)
    val = ""
    for i in range(n):
        if i%2 == 0:
            # appending the PT
            val += a[i]
        else:
            # appending XOR of key and roll no.
            val += XOR(b[i], rn[i%len(rn)])
    return val

# to get original char text from binary
def revive_text(text):
    str_data = ""
    for i in range(0, len(text), 8):
        temp_data = text[i:i + 8]
        decimal_data = int(temp_data, 2)
        str_data = str_data + chr(decimal_data)
    return str_data

# helper function which perfeorms the encryption process
def feistal_encrypt(pt, rounds=2):
    n = len(pt)
    L = pt[:n//2]
    R = pt[n//2:]
    f = open('BT18CSE107_keys.txt','w')
    for _ in range(rounds):
        # generating key = size of PT/2
        key = generate_key(n//2)
        f.write(key + '\n')
        L_new = R
        R_new =  XOR(L, round_func(R, key))
        L = L_new
        R = R_new
    
    f.close()

    return L + R


if __name__ == '__main__':     
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

    # Enter input file which is to be sent. 
    # Put 'exit' in the end to denote EOF
    f = open('../input.txt', 'r')
    for line in f.readlines():
        PT = line.strip()
        pt = ""

        if PT == "exit":
            print("Closing connection with ", host)
            conn.send(PT.encode())
            conn.close()
            break

        for i in PT:
            pt += binary_padded(i, 8)
        
        ct = feistal_encrypt(pt)
        cipher_text = revive_text(ct)
            
        print("\nPlain Text Sent: " , PT)
        print("Cipher Text: ", cipher_text)
        conn.send(ct.encode())
        time.sleep(0.25)
    f.close()







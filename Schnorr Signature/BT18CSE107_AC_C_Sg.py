'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import time
import socket            
import random
from sys import argv
from BT18CSE107_AC_C_Kg import fast_exponentiation

def hash_function(pt):
    return pt % 23

if __name__ == '__main__':     
    s = socket.socket()        
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

    s.bind((host, port))         
    print ("socket binded to %s" %(port))
    
    s.listen(5)    
    print ("socket is listening")           
  
    c, addr = s.accept()    
    print ('Got connection from', addr )

    f = open("BT18CSE107_public_keys.txt", 'r')
    line = f.readline()
    e1,e2,p,q = line.split(',')
    e1,e2,p,q = int(e1),int(e2), int(p) , int(q)
    f.close

    f1 = open("BT18CSE107_secret_keys.txt", 'r')
    d = int(f1.readline())
    f1.close()

# Reading input from file
# 'exit' at end to stop the connection
    f = open('../input.txt', 'r')
    for line in f.readlines():
        msg = line.strip()
        pt = ""

        # exiting condition
        if msg == "exit":
            c.send(msg.encode())
            c.close()
            break

        # converting msg to ASCII value 
        for i in msg:
            con = ord(i)
            if con < 10:
                pt += '0'
            pt += str(con)

        r = random.randint(1, q-1)
       
        val = fast_exponentiation(e1, r, p)
        val = val % p
        new_m = pt + str(val)

        s1 = hash_function(int(new_m))
        s2 = r + (d * s1) % q

        sending_string = str(s1) + "," + str(s2) + "," + pt
        print("\nSending to verifier: ", msg)
        print("S1 : ", s1, "\tS2 :", s2, "\tPlain Text: ", pt)
        c.send(sending_string.encode())

        time.sleep(0.25)
    f.close()
    
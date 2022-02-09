'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

import socket    
from sys import argv
from BT18CSE107_AC_C_Sg import hash_function        
from BT18CSE107_AC_C_Kg import fast_exponentiation

# Computing multiplicative inverse using extended euclidean
def euclidean(a,b):
    m = b
    if b == 0:
        d = a
        x = 1
        y = 0
        return (d,x,y)
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while b > 0:
        q = a//b
        r = a - q*b
        x = x2 - q*x1
        y = y2 - q*y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    d = a
    x = x2
    y = y2

    if x < 0:
        x += m
    return(d,x,y)

def multiplicative_inverse(a,m):
    d,x,y = euclidean(a,m)

    if d > 1:
        return(0)
    else:
        return(x)

if __name__ == '__main__':
# Create a socket object
    s = socket.socket()        
    
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
    s.connect((host, port))
    print("Connected to host: ", host) 
    
    while True:
    # receive data from the server and decoding to get the string.
        input_string = s.recv(1024).decode()
        if input_string == "exit":
            s.close()
            break
        
        s1, s2, m = input_string.split(",")
        s1, s2 = int(s1), int(s2)

        f = open("BT18CSE107_public_keys.txt", 'r')
        line = f.readline()
        e1,e2,p,q = line.split(',')
        f.close()

        e1,e2,p,q = int(e1),int(e2), int(p) , int(q)

        v1 = fast_exponentiation(e1, s2, p)

        v2 = fast_exponentiation(e2, s1 ,p)
        v2_inv = multiplicative_inverse(v2,p)
        v = ((v1 % p) * (v2_inv % p)) % p  
        m_v = m + str(v)

        v = hash_function(int(m_v))
        if v == s1:
            print("\nV computed: ", v, "\tS1 received: ", s1)
            print("Message received correctly!")
        else:
            print("\nV computed: ", v, "\tS1 received: ", s1)
            print("Faulty message")
       
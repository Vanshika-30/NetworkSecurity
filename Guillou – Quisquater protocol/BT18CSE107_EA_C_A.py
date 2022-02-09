'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107 
'''

import socket, random
from sys import argv
from BT18CSE107_EA_C_Kg import fast_exponentiation

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
    print ("socket binded to %sock" %(port))
    
    sock.listen(5)    
    print ("socket is listening")           
  
    conn, addr = sock.accept()    
    print ('Got connection from', addr )

    f = open("BT18CSE107_public.txt", 'r')
    lines = f.readline()
    f.close()
    n,e,v = lines.split(" ")
    n,e,v = int(n), int(e), int(v)

    f = open("BT18CSE107_private.txt", 'r')
    sk = f.readline()
    f.close()
    sk = int(sk)
    
    no_of_rounds = int(conn.recv(2048).decode())
    
    for i in range(no_of_rounds):
        print("\n----- Challenge Round ",i+1, "-----")
        r = random.randint(1,n)

        x = fast_exponentiation(r,e,n)
        conn.send(str(x).encode())

        challenge_c = conn.recv(2048).decode()
        print("Challenge c received: ", challenge_c)
        
        if challenge_c == "NA":
            conn.close()
            print("Failed, Invalid person")
            break
        
        challenge_c = int(challenge_c)
        y = (r * fast_exponentiation(sk,challenge_c, n) )% n

        conn.send(str(y).encode())
        print("X sent: ", x, "\tY sent: ", y)

    print("\nAll challenges passed! Authentication successful!!")
    conn.close()

'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

from random import randint
import socket
from sys import argv
from BT18CSE107_EA_C_Kg import fast_exponentiation

if __name__ == '__main__':
    # Create a socket object
    sock = socket.socket()        

    # Define the port on which you want to connect
    port = 12345
    host = 'localhost'
    no_of_rounds = 8

    keys = ["--host=","--port=","-h=","-p=", "--rounds=", "-r="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--host=' or key == '-h=':
                    host = argv[i][len(key):]
                elif key == '--port=' or key == '-p=':
                    port = int(argv[i][len(key):]) 
                elif key == '--rounds=' or key == '-r=':
                    no_of_rounds = int(argv[i][len(key):])
    
    # connect to the server on local computer
    sock.connect((host, port))
    print("Connected to host: ", host) 

    f = open("BT18CSE107_public.txt", 'r')
    lines = f.readline()
    f.close()
    n,e,v = lines.split(" ")
    n,e,v = int(n), int(e), int(v)

    sock.send(str(no_of_rounds).encode())
    
    # receive data from the server and decoding to get the string.
    for i in range(no_of_rounds):
        print("\n----- Challenge Round ", i+1 , "-----")
        
        x = sock.recv(2048).decode()
        x = int(x)
        challenge_c = randint(1,e)
        print("Challenge c sent: ", challenge_c)
        
        sock.send(str(challenge_c).encode())

        y = sock.recv(2048).decode()
        y = int(y)
        val = fast_exponentiation(y,e,n) * fast_exponentiation(v,challenge_c,n)
        val = val % n
        if val == x:
            print("Round verified!")
            print("X Received: ", x , "\tComputed Value: ", val)
        else:
            print("Failed to authenticate! Challenge Failed")
            sock.send("NA".encode())
            sock.close()
            
    print("\nAll challenges passed! Authentication successful!!")
    sock.close()

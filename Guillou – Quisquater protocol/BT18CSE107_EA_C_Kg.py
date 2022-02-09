'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

# pip install pycryptodome
from Crypto.Util.number import getPrime
from random import randint
from math import sqrt
from sys import argv

def fast_exponentiation(x, y, p = float('inf')):
    res = 1  
    x = x % p
     
    if (x == 0) :
        return 0
 
    while (y > 0) :
        if ((y & 1) == 1) :
            res = (res * x) % p

        y = y >> 1     
        x = (x * x) % p
    
    return res

def Euclidean(a,b):
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

def multiplicativeInverse(a,m):
    d,x,y = Euclidean(a,m)

    if d <= 1:
        return x

if __name__ == '__main__':
    N = 8
    keys = ["--key_size=", "-ks="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--key_size=' or key == '-ks=' :
                    N = int(argv[i][len(key):])
                
    p = getPrime(N)
    q = getPrime(N)
    
    while p == q:
        q = getPrime(N)

    n = p*q
    phi = (p-1)*(q-1)
    # e * phi = 1 mod n
    phi_inv = multiplicativeInverse(phi, n)
    e  = phi_inv % n

    s = randint(1,n)
    s_pow_e = fast_exponentiation(s,e,n)
    s_inv = multiplicativeInverse(s_pow_e, n)
    v = s_inv % n

    f = open("BT18CSE107_public.txt", 'w')
    f.write(str(n) + " " + str(e) + " " + str(v))
    f.close()

    f = open("BT18CSE107_private.txt", 'w')
    f.write(str(s))
    f.close()
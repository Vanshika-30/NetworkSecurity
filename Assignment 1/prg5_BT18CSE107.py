"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg5.py a x n
    eg python prg5.py 5 596 1234
    ans = 1013
"""

from sys import argv
from math import inf

def primeFactorize(n):
    factors = []
    count = 0
    while ((n % 2 > 0) == False):
        n >>= 1
        count += 1
 
    if (count > 0):
        factors.append([2,count])
 
    i = 3
    count = 0
    while i*i <= n:
        count = 0
        while (n % i == 0):
            count += 1
            n = n // i
        if (count > 0):
            factors.append([i,count])
            count=0
        i += 2
 
    if (n > 2):
        factors.append([n,count+1])

    return factors

def fastExponentiation(x, y, p=inf) :
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

def eulerTotient(n):
    prime_factors = primeFactorize(n)
    ans = 1
    for p,k in prime_factors:
        ans *= (fastExponentiation(p, k) - fastExponentiation(p, k-1))
    return int(ans)

# Converting decimal to binary string
def binary(x):
    k = ""
    while(x >= 1):
        t = x%2
        if t == 0:
            k += '0'
        else:
            k += '1'
        x = x//2
    return k

# Fermant Theorem to compute 𝑎^(𝑥)(𝑚𝑜𝑑 𝑛)
def fermat(a,x,n):
    b = 1
    if (x == 0):
        return b
    A = a
    x = x % eulerTotient(n)
    k = binary(x)
    if k[0] == '1':
        b = a
    # print(0, k[0] , A , b)
    for i in range (1,len(k)):
        A = (A*A) % n
        if k[i] == '1':
            b = (A * b) % n
        # print(i, k[i] , A , b)
    return(b)


if __name__ == '__main__':
    a,x,n = argv[1], argv[2], argv[3]
    print(fermat(int(a),int(x),int(n)), end="")


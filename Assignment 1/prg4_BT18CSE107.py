"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg4.py m
"""

from sys import argv
from math import inf, sqrt

# GCD computation
def gcd(a,b):
    if (a == 0):
        return b
    return gcd(b % a, a)

# Find all factors of a number n
def factors(n):
    i = 1
    ans = []
    while i <= sqrt(n):
         
        if (n % i == 0) :
            ans.append(int(i))
            if (n / i != i) :
                ans.append(int(n/i))
        i = i + 1
    return ans

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

# Computing power
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

# To compute the number of RRSM terms
def eulerTotient(n):
    prime_factors = primeFactorize(n)
    ans = 1
    for p,k in prime_factors:
        ans *= ((fastExponentiation(p, k) - fastExponentiation(p, k-1)))
    return int(ans)

def RRSM(n):
    phi = eulerTotient(n)
    factor = factors(n)

    if len(factor) == 2:
        if factor[0] == 1 and factor[1] == n:
            for i in range (1,n):
                print(i, end=" ")
            print(n-1, end="")
    else:
        for i in range(1,n):
            for j in factor:
                if i % j == 0:
                    if (gcd(i,n) == 1):
                        print(i, end=" ")
                    break 
    
        print(phi, end="")

if __name__ == '__main__':
    n=int(argv[1])
    RRSM(n)
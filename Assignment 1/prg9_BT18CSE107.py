"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg9.py a m
    
    eg: python3 prg9.py 4 7
    o/p: 3
"""

from sys import argv
from math import sqrt, inf

def gcd(a,b):
    if (a == 0):
        return b
    return gcd(b % a, a)

def getDivisors(n) :
    i = 1
    ans = []
    while i <= sqrt(n):
         
        if (n % i == 0) :
            ans.append(int(i))
            if (n / i != i) :
                ans.append(int(n/i))
        i = i + 1
    
    ans.sort()    
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
        count=0

    return factors

def fastExponentiation(x, y, mod=float('inf')) :
    res = 1  
    x = x % mod
     
    if (x == 0):
        return 0
 
    while (y > 0):
        if ((y & 1) == 1):
            res = (res * x) % mod

        y = y >> 1
        x = (x * x) % mod
    
    return res


def eulerTotient(n):
    prime_factors = primeFactorize(n)
    ans = 1
    for p,k in prime_factors:
        ans *= (fastExponentiation(p, k) - fastExponentiation(p, k-1))
    return int(ans)

# Function to find order of a under modulo m
def order(a, factors, m):
    prev = a
    curr = 0
    if prev % m == 1:
        print("1", end="")
    else:
        for i in range(1,len(factors)):
            curr = pow(a,factors[i]-factors[i-1])
            if (curr*prev) % m == 1:
                print(factors[i], end="")
                break
            prev=(curr*prev)%m

if __name__ == '__main__' :
    a,m = int(argv[1]),int(argv[2])

    if gcd(a,m) != 1:
        print("-1")
    else:
        # Using euler totient function to find phi(m)
        phim = eulerTotient(m)
        factors = getDivisors(phim)
        
        order(a, factors, m)

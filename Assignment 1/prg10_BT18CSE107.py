"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg10.py m
"""

from sys import argv
from math import sqrt

def gcd(a,b):
    if (a == 0):
        return b
    return gcd(b % a, a)

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


def fastExponentiation(x, y, p = float('inf')):
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

def getDivisors(n):
    i = 1
    ans = []
    while i <= sqrt(n):
         
        if (n % i == 0) :
            ans.append(int(i))
            if (n / i != i) :
                ans.append(int(n/i))
        i = i + 1
    return ans

def RRSM(n):
    ans = []
    factor = getDivisors(n)

    if len(factor) == 2:
        if factor[0] == 1 and factor[1] == n:
            for i in range (1,n):
                ans.append(i)
    else:
        for i in range(1,n):
            for j in factor:
                if i % j == 0:
                    if (gcd(i,n) == 1):
                        ans.append(i)
                    break
    return ans

def powMod(a,b,p):
    res = 1
    while b != 0:
        if (b%2 == 1):
            res = int (res * 1 * a % p)
            b-=1
        else:
            a = int(a * 1 * a % p)
            b = b//2
    return res

# funtion to find all the primitive roots
def primitiveRoots(p):
    fact = []
    phi = eulerTotient(p)  
    rrsm_m = RRSM(p)
    n = phi
    i=2
    while i*i <= n:
        if(n % i == 0):
            fact.append(i)
            while (n % i == 0):
                n= n//i
        i+=1
        
    if(n > 1):
        fact.append(n)

    ans = []
    for curr in rrsm_m:
        ok = True
        i=0
        while i < len(fact) and ok == True:
            ok &= powMod(curr, phi / fact[i], p) != 1
            i+=1
        if(ok):
            ans.append(curr)
    return ans

if __name__ == '__main__':
    m = int(argv[1])
    ans = primitiveRoots(m)
    sz = len(ans)
    if sz == 0:
        print(sz, end="")
    else:
        print(len(ans),end=" ")
        for i in range(sz):
            if i != sz-1:
                print(ans[i],end=" ")
            else:
                print(ans[i], end="")
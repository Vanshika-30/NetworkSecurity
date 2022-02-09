'''
    Name: Vanshika Jain
    Roll No.: BT18CSE107
'''

# pip install pycryptodome
from Crypto.Util.number import getPrime
from math import sqrt
from sys import argv
import random

def GCD(a,b):
    if (a == 0):
        return b
    return GCD(b % a, a)

def prime_factorize(n):
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

def euler_totient(n):
    prime_factors = prime_factorize(n)
    ans = 1
    for p,k in prime_factors:
        ans *= (fast_exponentiation(p, k) - fast_exponentiation(p, k-1))
    return int(ans)

def get_divisors(n):
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
    factor = get_divisors(n)

    if len(factor) == 2:
        if factor[0] == 1 and factor[1] == n:
            for i in range (1,n):
                ans.append(i)
    else:
        for i in range(1,n):
            for j in factor:
                if i % j == 0:
                    if (GCD(i,n) == 1):
                        ans.append(i)
                    break
    return ans

def pow_mod(a,b,p):
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
def primitive_roots(p):
    fact = []
    phi = euler_totient(p)  
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
            ok &= pow_mod(curr, phi / fact[i], p) != 1
            i+=1
        if(ok):
            ans.append(curr)
    return ans

if __name__ == '__main__':
    N = 8
    keys = ["--key_size=","-ks="]                                                                                                           
    for i in range(1,len(argv)):                                                                                                       
        for key in keys:                                                                                                                   
            if argv[i].find(key) == 0:                                                                                                 
                if key == '--key_size=' or key == '-ks=':
                    N = int(argv[i][len(key):])
                

    # generating 2 primes p and q
    p = getPrime(N)
    
    factor = prime_factorize(p-1)
    q = random.choice(factor)[0]
    
    zp = primitive_roots(p)
    e0 = random.choice(zp)
    while e0 == 1:
        e0 = random.choice(zp)
    
    e1 = fast_exponentiation(e0, int((p-1)/q),  p)
    e1 = e1 % p
    
    d = random.choice(zp)
    e2 = fast_exponentiation(e1, d, p)
    e2 = e2 % p

    f = open("BT18CSE107_public_keys.txt", 'w')
    f.write(str(e1) + "," + str(e2) + "," + str(p) + "," + str(q))
    f.close

    f1 = open("BT18CSE107_secret_keys.txt", 'w')
    f1.write(str(d))
    f1.close

    print("PUBLIC KEY: ", e1, e2, p, q)
    print("SECRET KEY: ", d)
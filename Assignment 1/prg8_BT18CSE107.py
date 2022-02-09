"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg8.py a b m
    
    eg:
    python3 prg8.py 1 606 138 1710
    Y 178 463 748 1033 1318 1603

    python3 prg8.py 3 2 5 7 4 2 6 1 3 5    
    Y 83 188
"""

from sys import argv

def gcd(a, b):
     
    if (a == 0):
        return b
         
    return gcd(b % a, a)
 
def lcm(a, b):
     
    return (a * b) // gcd(a, b)
 
# check if all elements of an array are pairwise coprime
def checkPairwiseCoPrime(A, n):
     
    prod = 1
    l = 1
 
    for i in range(n):
 
        prod *= A[i]
 
        l = lcm(A[i], l)
    if (prod == l):
        return 1
    else:
        return 0

# Inverse via extended euclidean
def multiplicativeInverse(a, b):
    m = b
    if b == 0:
        return (a, 1,0)
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
    g = a
    x = x2
    y = y2
    return (x % m + m)%m

# Utility function to compute all possible solutions
def CRTUtil(a,b,m,i,ans, a_i):
    if i == len(a):
        M = 1
        for mi in m:
            M *= mi
        temp = 0
        for i in range (len(a)):
            temp += ((M//m[i]) * a_i[i] * multiplicativeInverse(M//m[i], m[i])) % M
            temp %= M
        ans.append(temp)
        return
    else:
        g = gcd(a[i], m[i])
        if g == 1:
            a_i.append((b[i] * multiplicativeInverse(a[i],m[i])) % m[i])
            CRTUtil(a,b,m,i+1, ans, a_i)
            a_i.pop()
        else:
            x = ((b[i] * multiplicativeInverse(a[i]//g ,m[i]//g))//g )  % m[i]
            for j in range (g):
                a_i.append((x + (j*m[i]) // g) % m[i])
                CRTUtil(a,b,m,i+1, ans, a_i)
                a_i.pop()

# Using Chinese Remainder Theorem to find solution of congruence
def CRT(a,b,m):
    if(checkPairwiseCoPrime(m, len(m))):
        ans = []
        CRTUtil(a,b,m,0, ans, [])
        return ans
    else:
        return "N"

if __name__ == '__main__':
    n = int(argv[1])
    a = [0]*n
    b = [0]*n
    m = [0]*n
    j = 2
    i = 0
    while i < n:
        a[i] = int(argv[j])
        j+=1
        b[i] = int(argv[j])
        j+=1
        m[i] = int(argv[j])
        j+=1
        i+=1

    # If in any one equation, the gcd of a and m does not divide b then the 
    # equations dont have a solution
    for i in range (len(a)):
        g = gcd(a[i], m[i])
        if b[i] % g != 0:
            print("N", end="")
            break
    else:
        ans = CRT(a,b,m)
        if ans != "N":
            ans.sort()
            print("Y", end=" ")
            sz = len(ans)
            i = 0
            while i != sz-1:
                print(ans[i], end=" ")
                i+=1
            print(ans[i], end="")
        else:
            print(ans, end="")
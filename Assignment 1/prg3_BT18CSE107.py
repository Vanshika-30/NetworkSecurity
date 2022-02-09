"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg3.py n
"""

import math
from sys import argv

# Prime Factorization
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
            count = 0
        i += 2
 
    if (n > 2):
        factors.append([n,count+1])

    return factors

if __name__ == '__main__':
    n=int(argv[1])
    factor = primeFactorize(n)
    for i in range(len(factor)-1):
        while factor[i][1]:
            print(factor[i][0], end=" ")
            factor[i][1]-=1

    i+=1
    while factor[i][1] != 1:
            print(factor[i][0], end=" ")
            factor[i][1]-=1
    print(factor[i][0], end="")
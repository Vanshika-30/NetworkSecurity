"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg1.py n a1 a2 a3 ..... an
"""

from sys import argv
from math import sqrt

# Function to compute gcd
def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)

# Function to print all divisors of a number
def factors (n):
    i = 1
    sq=int(sqrt(n))
    while (i <= sq):
        if (n % i == 0):
            print(i, end=" ")
        i += 1
        
    ans = []
    if n>1:
        for i in range(sq, 0, -1):
            if (n % i == 0):
                ans.append(n // i)

    for i in range(len(ans) - 1):
        print(ans[i], end=" ")

    print(ans[i+1], end="")

# Util function
def printAllDivisors(arr, N):
    g = arr[0]

    for i in range(1, N):
        g = gcd(arr[i], g)

    factors(g)


if __name__ == '__main__':
    n=int(argv[1])
    arr=[0]*n
    for i in range(2,len(argv)):
        arr[i-2] = int(argv[i])

    printAllDivisors(arr, n)
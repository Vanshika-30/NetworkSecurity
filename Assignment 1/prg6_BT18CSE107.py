"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg6.py a m

    eg : python3 prg6.py 3 11
    ans =  Y 4
"""

from sys import argv
# Computing multiplicative inverse using extended euclidean

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

    if d > 1:
        print("N", end="")
    else:
        print("Y", end=" ")
        print(x , end="")

if __name__ == '__main__':
    a,m = argv[1], argv[2]
    multiplicativeInverse(int(a),int(m))

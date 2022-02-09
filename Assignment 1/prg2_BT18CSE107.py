"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg2.py a b
"""

from sys import argv

# Extended Euclidean function
def Euclidean(a,b):
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
    return(g, x,y)

if __name__ == '__main__':
    a,b = argv[1], argv[2]
    g,x,y = Euclidean(int(a), int(b))
    print(x,y, end="")

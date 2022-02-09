"""
Name: Vanshika Jain
Roll No.: BT18CSE107

Instruction to run:
    python prg7.py a b m
    
    eg: python prg7.py 606 138 1710
    o/p: Y 6 178 463 748 1033 1318 1603
"""

from sys import argv

def Euclidean(a, b):
     
    if a == 0 :
        return b, 0, 1
         
    gcd, x1, y1 = Euclidean(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
     
    return gcd, x, y
     
# Function to give the distinct solutions of ax = b (mod n)
def linearCongruence(A, B, M):
    A = A % M
    B = B % M
    x = 0
    y = 0

    g, x, y = Euclidean(A, M)
     
    if (B % g != 0):
        print("N")
        return "N"
     
    print("Y",end=" ")
    x0 = (x * (B // g)) % M
    if (x0 < 0):
        x0 += M
     
    ans = []
    for i in range(g):
        ans.append((x0 + i * (M // g)) % M)
    
    return ans
    

if __name__ == '__main__':
    a,b,m = int(argv[1]),int(argv[2]),int(argv[3])
    ans = linearCongruence(a,b,m)
    if ans != "N":
        ans.sort()
        sz = len(ans)
        if sz==0:
            print(sz,end='')
        else:
            print(sz,end=" ")
            for i in range(sz):
                if i!=sz-1:
                    print(ans[i],end=" ")
                else:
                    print(ans[i],end='')
    
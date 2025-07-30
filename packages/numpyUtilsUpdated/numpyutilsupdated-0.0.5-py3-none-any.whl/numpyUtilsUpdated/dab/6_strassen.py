code="""
def strassen(A, B): 
    n = len(A) 
    if n == 1: 
        return [[A[0][0] * B[0][0]]] 
    half = n // 2 
    A11 = [row[:half] for row in A[:half]] 
    A12 = [row[half:] for row in A[:half]] 
    A21 = [row[:half] for row in A[half:]] 
    A22 = [row[half:] for row in A[half:]] 
    B11 = [row[:half] for row in B[:half]] 
    B12 = [row[half:] for row in B[:half]] 
    B21 = [row[:half] for row in B[half:]] 
    B22 = [row[half:] for row in B[half:]] 
    P1 = strassen(A11, B11) 
    P2 = strassen(A12, B21) 
    P3 = strassen(A11, B12) 
    P4 = strassen(A12, B22) 
    P5 = strassen(A21, B11) 
    P6 = strassen(A22, B21) 
    P7 = strassen(A21, B12) 
    C11 = [[P1[i][j] + P2[i][j] for j in range(half)] for i in range(half)] 
    C12 = [[P3[i][j] + P4[i][j] for j in range(half)] for i in range(half)] 
    C21 = [[P5[i][j] + P6[i][j] for j in range(half)] for i in range(half)] 
    C22 = strassen(A22, B22) 
    C22 = [[C22[i][j] + P7[i][j] for j in range(half)] for i in range(half)] 
    C = [[0] * n for _ in range(n)] 
    for i in range(half): 
        for j in range(half): 
            C[i][j] = C11[i][j] 
            C[i][j + half] = C12[i][j] 
            C[i + half][j] = C21[i][j] 
            C[i + half][j + half] = C22[i][j] 
    return C 

n = int(input("Enter n (power of 2): ")) 
A = [] 
B = [] 
print("Enter first matrix:") 
for _ in range(n): 
    A.append(list(map(int, input().split()))) 
print("Enter second matrix:") 
for _ in range(n): 
    B.append(list(map(int, input().split()))) 
C = strassen(A, B) 
print("Result Matrix:") 
for row in C: 
    print(' '.join(map(str, row)))
"""
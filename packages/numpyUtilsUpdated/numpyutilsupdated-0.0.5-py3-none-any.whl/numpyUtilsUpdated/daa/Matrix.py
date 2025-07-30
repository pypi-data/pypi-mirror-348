import numpy as np

def strassen(A, B):
    n = len(A)
    new_size = 1
    while new_size < n:
        new_size *= 2
    if new_size > n:
        A = np.pad(A, ((0, new_size - n), (0, new_size - n)), mode='constant')
        B = np.pad(B, ((0, new_size - n), (0, new_size - n)), mode='constant')
    
    def strassen_rec(A, B):
        n = len(A)
        if n == 1:  
            return A * B
        if n == 2: 
            return np.dot(A, B)
        
        mid = n // 2
        A11 = A[:mid, :mid]
        A12 = A[:mid, mid:]
        A21 = A[mid:, :mid]
        A22 = A[mid:, mid:]
        B11 = B[:mid, :mid]
        B12 = B[:mid, mid:]
        B21 = B[mid:, :mid]
        B22 = B[mid:, mid:]

        P1 = strassen_rec(A11, B12 - B22)
        P2 = strassen_rec(A11 + A12, B22)
        P3 = strassen_rec(A21 + A22, B11)
        P4 = strassen_rec(A22, B21 - B11)
        P5 = strassen_rec(A11 + A22, B11 + B22)
        P6 = strassen_rec(A12 - A22, B21 + B22)
        P7 = strassen_rec(A11 - A21, B11 + B12)
        
        C11 = P5 + P4 - P2 + P6
        C12 = P1 + P2
        C21 = P3 + P4
        C22 = P5 + P1 - P3 - P7
        
        C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
        return C
    
    C_padded = strassen_rec(A, B)
    
    C = C_padded[:n, :n]
    
    return C

A = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
B = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
C = strassen(A, B)
print("Matrix C (Result of A * B):\n", C)

code = '''
import numpy as np

def strassen(A, B):
    n = len(A)
    new_size = 1
    while new_size < n:
        new_size *= 2
    if new_size > n:
        A = np.pad(A, ((0, new_size - n), (0, new_size - n)), mode='constant')
        B = np.pad(B, ((0, new_size - n), (0, new_size - n)), mode='constant')
    
    def strassen_rec(A, B):
        n = len(A)
        if n == 1:  
            return A * B
        if n == 2: 
            return np.dot(A, B)
        
        mid = n // 2
        A11 = A[:mid, :mid]
        A12 = A[:mid, mid:]
        A21 = A[mid:, :mid]
        A22 = A[mid:, mid:]
        B11 = B[:mid, :mid]
        B12 = B[:mid, mid:]
        B21 = B[mid:, :mid]
        B22 = B[mid:, mid:]

        P1 = strassen_rec(A11, B12 - B22)
        P2 = strassen_rec(A11 + A12, B22)
        P3 = strassen_rec(A21 + A22, B11)
        P4 = strassen_rec(A22, B21 - B11)
        P5 = strassen_rec(A11 + A22, B11 + B22)
        P6 = strassen_rec(A12 - A22, B21 + B22)
        P7 = strassen_rec(A11 - A21, B11 + B12)
        
        C11 = P5 + P4 - P2 + P6
        C12 = P1 + P2
        C21 = P3 + P4
        C22 = P5 + P1 - P3 - P7
        
        C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
        return C
    
    C_padded = strassen_rec(A, B)
    
    C = C_padded[:n, :n]
    
    return C

A = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
B = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
C = strassen(A, B)
print("Matrix C (Result of A * B):\n", C)
'''

def getCode():
    global code
    print(code)
    
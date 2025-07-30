code = '''

import numpy as np

def S_Mat(A, B):
    n = len(A)
    
    if n == 1:
        return A * B
    
    mid = n//2
    
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]
    
    M1 = S_Mat(A11 + A22, B11 + B22)
    M2 = S_Mat(A21 + A22, B11)
    M3 = S_Mat(A11, B12 - B22)
    M4 = S_Mat(A22, B21 - B11)
    M5 = S_Mat(A11 + A12, B22)
    M6 = S_Mat(A21 - A11, B11 + B12)
    M7 = S_Mat(A12 - A22, B21 + B22)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))

if __name__ == "__main__":
    A = np.array([
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [3, 3, 3, 3],
        [2, 2, 2, 2]
        ])
    B = np.array([
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [3, 3, 3, 3],
        [2, 2, 2, 2]
        ])

    result = S_Mat(A, B)
    print("Strassen's Matrix Multiplication Result:")
    print(result)

'''
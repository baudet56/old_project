
def mult_matrice(matrice_A,matrice_B):
    l = len(matrice_A)
    C = [ [0 for i in range(l)] for i in range(l)]
    for i in range(l):
        for j in range(l):
            for k in range(l):
                C[j][i] = C[j][i] + matrice_A[j][k] *matrice_ B[k][i]
    return C

def mult_scal(matrice_A,scal):
    l = len(matrice_A)
    B = [ [0 for i in range(l)] for i in range(l)]
    for y in range(l):
        for x in range(l):
                B[x][y] = matrice_A[x][y] * scal
    return B

def add_matrice(matrice_A,matrice_B):
    l = len(matrice_A)
    c = [ [0 for i in range(l)] for k in range(l)]
    for i in range(l):
        for k in range(l):
                c[i][k] = matrice_A[i][k] + matrice_B[i][k]
    return c
    
def identity(taille):
    A = [[0 for i in range(taille)]for i in range(taille)]
    for i in range(k):
        A[i][i] = float(1)
    return A





grille = [ [0, 4, 0,  1, 0, 0,  0, 0, 0], 
           [0, 0, 3,  5, 0, 0,  0, 1, 9], 
           [0, 0, 0,  0, 0, 6,  0, 0, 3],

           [0, 0, 7,  0, 0, 5,  0, 0, 8],
           [0, 8, 1,  0, 0, 0,  9, 6, 0],
           [9, 0, 0,  2, 0, 0,  7, 0, 0],

           [6, 0, 0,  9, 0, 0,  0, 0, 0],
           [8, 1, 0,  0, 0, 2,  4, 0, 0],
           [0, 0, 0,  0, 0, 4,  0, 9, 0] ]

      

posibility = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for i in range(9)] for j in range(9)]
number = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def colone(j, L = grille):
   C = []
   for ligne in grille:
      C.append(ligne[j])
   return C



def clear():
   for i in range(9):
      for j in range(9):
         if grille[i][j] != 0:
            posibility[i][j] = [0]


def check_ligne(i):
   for n in number:
      if n in grille[i]:
         for j in range(9):
            if n in posibility[i][j]:
               posibility[i][j].remove(n)

def check_row(j):
   for n in number:
      if n in colone(j):
         for i in range(9):
            if n in posibility[i][j]:
               posibility[i][j].remove(n)

def check_case(ic,jc):
   i = 3*ic
   j = 3*jc
   L = []
   for a in range(i,i+3):
      for b in range(j,j+3):
         L.append(grille[a][b])
   for n in number:
      if n in  L:
         for a in range(i,i+3):
            for b in range(j,j+3):
               if n in posibility[a][b]:
                  posibility[a][b].remove(n)

def finish():
   for i in range(9):
      for j in range(9):
         if grille[i][j] == 0: return False
   return True

def check_2(ic,jc):
   i, j = ic*3, jc*3
   L = [0 for i in range(10) ]
   for a in range(i,i+3):
      for b in range(j,j+3):
         for k in range(10):
                 if k in posibility[a][b]: L[k] += 1
   for g in range(1, 10):
      if L[g] == 2:
         R = [] 
         for a in range(i,i+3):
            for b in range(j,j+3):
               if g in posibility[a][b]: R.append([a,b])

         if R[0][0] == R[1][0]:
            for i1 in range(9):
               if g in posibility[R[0][0]][i1] and i1 != R[0][1] and i1 != R[1][1]:
                  posibility[R[0][0]][i1].remove(g)
   
         if R[0][1] == R[1][1]:
            for j1 in range(9):
               if g in posibility[j1][R[1][1]] and j1 != R[0][0] and j1 != R[1][0]:
                  posibility[j1][R[1][1]].remove(g)


def complete():

   for ic in range(3):
         for jc in range(3):
            for n in number:
               cpt = 0
               for i in range(3*ic, 3*ic + 3):
                  for j in range(3*jc, 3*jc + 3):
                     if n in posibility[i][j]:
                        cpt += 1
         if cpt == 1:
            for i in range(3*ic, 3*ic + 3):
               for j in range(3*jc, 3*jc + 3):
                  if n in posibility[ic][jc]: posibility[ic][jc] = [n]

   for k in range(9):
      for n in number:
         cpt_ligne = 0
         cpt_row   = 0
         for a in range(9):
            if n in posibility[k][a]:
               cpt_ligne += 1
            if n in posibility[a][k]:
               cpt_row += 1
         if cpt_ligne == 1:
            for a in range(9):
               if n in posibility[k][a]: posibility[k][a] = [n]
         if cpt_row == 1:
            for a in range(9):
               if n in posibility[a][k]: posibility[a][k] = [n]


      

      

      for i in range(9):
         for j in range(9):
            if len(posibility[i][j]) == 1 and posibility[i][j] != [0]:
               grille[i][j] = posibility[i][j][0]



def affichage(L = grille):
   for i in range(9):
      txt = ''
      for j in range(9):
         if type(L[i][j]) == list:
            k = 6-len(L[i][j])
         else : k = 0
         txt += ' ' + str(L[i][j]) + k*' '
         if (j + 1)%3 == 0:
            txt += ' '
      if (i+1)%3 == 0:
         txt += '\n'
      print(txt)


clear()
affichage()
cpt = 0
while not finish():

   for k in range(9):
      check_ligne(k)
      check_row(k)
   for ic in range(3):
      for jc in range(3):
         check_case(ic,jc)
         check_2(ic, jc)
   complete()
   clear()
   if cpt == 500:
      print('___________________________ \n')
      affichage()
      affichage(posibility)
   cpt += 1
print('\n','solution:','\n')
affichage()

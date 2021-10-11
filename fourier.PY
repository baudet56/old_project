# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Mise en évidence animée de la convergence d'une série de Fourier
# Jean-Philippe COSTES - Lycée LESAGE - Janvier 2015
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from random import random
#-------------------------------------------------------------------------------
# Définition de fonctions périodiques standards f(t)
# et calcul analytique de ses coefficients (a_k, b_k, c_k)
#-------------------------------------------------------------------------------
# définition d'un choix parmi toutes les fonctions construites
#-------------------------------------------------------------------------------
print(" ---------------------------------------------------------------------")
print(" Fonctions disponibles:")
print(" ---------------------------------------------------------------------")
print(" 1 - fonction rect. symétrique centrée d'amplitude A, de période T,")
print(" 2 - fonction sinus filtré (1/2 sinus sur [0, T/2], valeur nulle sur [T/2, T])")
print(" 3 - fonction sinus redressé (la fonction a une fréquence double !),")
print(" 4 - fonction dents de scie d'amplitude A, de période T,")
print(" 5 - fonction triangle d'amplitude A, de période T,")
print(" 6 - fonction MLI d'amplitude A, de période T, de rapport cyclique alpha.")
print(" 7 - fonction definie par liste de points ")

choix = int(input("Choisir un numéro de fonction parmi celles proposées : "))
print("La fonction choisie est la numéro :", choix)

#-------------------------------------------------------------------------------
# paramètres numériques pour les fonctions
#-------------------------------------------------------------------------------
A, T  = 1, 2
omega = 2*np.pi/T
alpha = 0.3     # rapport cyclique, utile seulement pour la fonction 6 (MLI)

#-------------------------------------------------------------------------------
# f1 - fonction rect. symétrique centrée d'amplitude A, de période T
#-------------------------------------------------------------------------------
if choix == 1:

    def f(t):
      t = t%T
      if t > T/2:
         return 0
      else:
         return A

#-------------------------------------------------------------------------------
# f2 - fonction sinus filtré (1/2 sinusoide [0,T/2] + valeur nulle sur [T/2,T])-----
#-------------------------------------------------------------------------------
if choix == 2:

    def f(t):
      t = t%T
      if t > T/2:
          return 0
      else:
          return A*np.sin(omega*t)


#-------------------------------------------------------------------------------
# f3 - fonction sinus redressé (la fonction a une fréquence double !)
#-------------------------------------------------------------------------------
if choix == 3:

    def f(t):
        t = t%T
        return abs(np.sin(1/2*omega*t))

#-------------------------------------------------------------------------------
# f4 - fonction dents de scie d'amplitude A, de période T
#-------------------------------------------------------------------------------
if choix == 4:

    def f(t):
        t = t%T
        return A * t/T 


#-------------------------------------------------------------------------------
# f5 - fonction triangle d'amplitude A, de période T
#-------------------------------------------------------------------------------
if choix == 5:
    def f(t):
      t = t%T
      if t > T/2:
          return  2 * A * (T - t)/T
      else:
          return 2*A *t/T

#-------------------------------------------------------------------------------
# f6 - fonction MLI d'amplitude A, de période T, de rapport cyclique alpha
#-------------------------------
if choix == 6:
    def f(t):
        t = t%T
        if t > alpha*T:
            return 0
        else:
            return A
if choix == 7:
    XY = [ [0.,0.], [1.5,2.5], [1.5,1.], [2.5,0.3], [4., 1.8], [5.,1.8] ]
    T = XY[-1][0]
    omega = 2*np.pi/T
    def f(t):
        t = t%T
        for l in range(1,len(XY)):
            a = XY[l]
            b = XY[l-1]
            if a[0] > t >= b[0]:
                return b[1] + (a[1] - b[1])/(a[0]-b[0])*(t-b[0])

a0 = 1/T*quad(f,0,T)[0]

def a_(k):
    return 2/T*quad(lambda t,k:  f(t)*np.cos(k*omega*t),0,T,args = (k))[0]

def b_(k):
    return 2/T * quad(lambda t,k:  f(t)*np.sin(k*omega*t),0,T,args = (k))[0]
#-------------------------------------------------------------------------------
# Choix d'un nombre d'harmoniques et construction des listes a_k, b_k et c_k
#--------+-----------------------------------------------------------------------

nMax = 20
a_k, b_k = [a0], [0] # initialisation des  listes 


for k in range(1, nMax + 1):
   a_k.append(a_(k))
   b_k.append(b_(k))

# conversion en tableaux pour vectorisation pour le calcul des c_k
a_k = np.array(a_k)
b_k = np.array(b_k)
c_k = np.sqrt(a_k**2 + b_k**2)

#-------------------------------------------------------------------------------
# C.3 Tracé du spectre en amplitude (an, bn en fonction de n)
#-------------------------------------------------------------------------------
listeN = np.array([i for i in range(nMax+1)])
delta  = 0.2 # épaisseur des barres pour l'affichage 

plt.ion()

plt.figure(1,figsize = (8,5))
plt.title('$Spectre\ en\ amplitude\ en \ fonction\ de\ l\'ordre\ de\ l\'harmonique$')

plt.xticks(np.arange(nMax+1))
plt.grid(True, ls = '-', alpha = 0.5)

plt.bar(listeN[1:]-delta, c_k[1:], color='green', alpha = 0.5, \
        width = 2*delta,label = r'$c_n$')

plt.bar(listeN[1:]-delta, a_k[1:], color='red'  , alpha = 0.8, \
        width = delta, label = r'$a_n$')

plt.bar(listeN[1:],       b_k[1:], color='blue' , alpha = 0.8, \
        width = delta, label = r'$b_n$')

plt.legend(loc = 1)

plt.show()

#-------------------------------------------------------------------------------
# Définition de la liste des dates pour le tracé
#-------------------------------------------------------------------------------
NbPe, NbPt = 3, 1000 # nombre de périodes, nombre de points/période (pour tracé)
Temps      = np.linspace(0,NbPe*T,NbPt*NbPe)

listeF = [f(i) for i in Temps]

#-------------------------------------------------------------------------------
# Définition de la somme partielle de la série partielle de Fourier à construire
#-------------------------------------------------------------------------------
def serie(n,t):
    S = a_k[0]+b_k[0]
    for k in range(1,n+1):
        S += a_k[k]*np.cos(k*omega*t)  + b_k[k]*np.sin(k*omega*t)
    return S

listeS = [serie(nMax,t) for t in Temps]

#-------------------------------------------------------------------------------
# C.4 Tracé de la somme des n premiers termes
#     de la série associée à la fonction périodique de référence
#-------------------------------------------------------------------------------

plt.figure(2)

plt.grid(True, ls = '-', color = 'grey')
plt.title('$Somme\ des\ (n)\ premiers\ termes\ de\ la\ série\ de\ Fourier$')

plt.plot(Temps, listeF , '-b', linewidth = 1.5)
plt.plot(Temps, listeS , '-r', linewidth = 1.)

plt.show()

from numpy import array,float64
from numba import jit
import numba
#import ctypes
G = 6.67e-11               #N.m²/Kg²

#--------------------------------------------Outils mathematique
@jit(numba.float64(numba.float64[:], numba.float64[:]),parallel=True , nopython = True)
def distance(Object_1,Object_2):
   distance_carré = (Object_1[0]-Object_2[0])**2 + (Object_1[1]-Object_2[1])**2
   return distance_carré**(1/2)


#@vectorize(['float64[:](float64[:],float64[:])'],target = 'cuda')
@jit(numba.float64[:](numba.float64[:], numba.float64[:]), nopython = True)
def vecteur(Object_1,Object_2):
   X, Y = Object_2[0] - Object_1[0], Object_2[1] - Object_1[1]
   return array([X,Y],dtype = float64)




#------------------------------------------------calcule integrale
@jit(numba.float64[:](numba.float64[:], numba.float64[:], numba.float64[:], numba.float64), nopython = True)
def Vitesse(Object, Acceleration, Acceleration_precedente, dt):
   V =[V_x, V_y] = [Object[2], Object[3]]
   V = array(V,dtype = float64)
   V = V + (Acceleration + Acceleration_precedente) * dt/2
   return V

@jit(numba.float64[:](numba.float64[:], numba.float64[:], numba.float64[:], numba.float32), nopython = True)
def position(Object, Acceleration_precedente, Vitesse_precedente,dt):
   Pos = [X, Y] = [Object[0], Object[1]]
   Pos = array(Pos,dtype=float64)
   Pos = Pos + Vitesse_precedente*dt + Acceleration_precedente*dt*dt/2
   return Pos

#--------------------------------------------Création Forces

#@jit(numba.float64[:](numba.float64[:], numba.types.pyobject))
#@jit
@jit(numba.float64[:](numba.float64[:], numba.types.pyobject))
def Gravite(Object_1, Object_List):
   Force_gravite = array([0, 0],dtype=float64)
   for Object in Object_List:
      if Object[-1] != Object_1[-1]: 
         d = distance(array(Object_1[0:2],dtype = float64), array(Object[0:2],dtype = float64))
         vec = vecteur(array(Object[0:2],dtype = float64), array(Object_1[0:2],dtype = float64))
         Norme_vec = distance(vec,array([0,0],dtype = float64))
         direction = array(vec,dtype=float64) / Norme_vec
         Norme = -G * Object[-3]/(d**2)
         Force_gravite = Force_gravite + Norme * direction
   return Force_gravite


#@jit
@jit(numba.float64[:](numba.float64[:], numba.types.pyobject))
def PFD(Object, Object_list):
   acceleration = array([0, 0])
   F_g = array(Gravite(Object, Object_list),dtype=float64)
   acceleration = acceleration + F_g
   return acceleration


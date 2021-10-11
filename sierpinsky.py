import turtle as tr
import numpy as np
tr.speed(0)
tr.up()
L, n = 100, 4
tr.goto(-L*2,-L*4)
tr.down()
global t
t = 3

global a_m
a_m = 360/t
def triangle(longueur):
    for i in range(t):
        tr.fd(longueur)
        tr.lt(a_m)

def sierpinsky_1(longueur):
    for i in range(3):
        triangle(longueur)
        tr.fd(longueur*2)
        tr.lt(a_m)


def sierpinsky_n(longueur,n):
    if n ==0:
        triangle(longueur)
    else:
        for i in range(t):
            sierpinsky_n(longueur/2,n-1)
            tr.fd(longueur)
            tr.lt(a_m)
    
sierpinsky_n(L,n)

import turtle as tr





def fract(L,n):
    if n ==0:
        tr.fd(L)
        return
    fract(L,n-1)
    tr.lt(60)
    fract(L,n-1)
    tr.rt(120)
    fract(L,n-1)
    tr.lt(60)
    fract(L,n-1)





L = 800
n = 6
tr.up()
tr.goto(-400,250)
tr.down()
tr.speed(0)
fract(L/3**n,n)
tr.rt(120)
fract(L/3**n,n)
tr.rt(120)
fract(L/3**n,n)
tr.mainloop()

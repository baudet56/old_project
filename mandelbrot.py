import matplotlib.pyplot as plt

N = 10000
nb_iter = 300


tab = [[0 for k in range(N)]for k in range(N)]

def test(x,y):
    z = x + y*1j
    z_n = z
    for k in range(nb_iter):
        z_n = z_n*z_n + z
        if abs(z_n) > 2:
            return 5*(k+1) + 50
    return 0
    

for i in range(N):
    for j in range(N):
        x = 0.5 - 2*i/N
        y = 1 - 2*j/N

        tab[j][i] = test(x, y)

plt.imshow(tab,'jet')
plt.colorbar()
plt.show()

            

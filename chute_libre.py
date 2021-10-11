import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# definition des variable 
# =============================================================================

m = 90      #Kg
Z_0 = 4000  #m
V_0 = 40    #m/s
Z_a = 1500  #m
B = [0.245,35.3,0.245] #Kg/m
g = 9.81    #m/s²
k = 0
t_ouv = 4   #temps d'ouverture du parachute




# =============================================================================
# definition des fonction 
# =============================================================================

def ax(vx,t,vz,k):
    #accélération selon l'axe Ux
    ax = -B[k]/m * np.sqrt(vx**2+vz**2)*vx
    return ax

def az(vz,t,vx,k):
    #accélération selon l'axe Uz
    az =  -B[k]/m * np.sqrt(vx**2+vz**2)*vz - g
    return az


    


def Fx(X,Z,t,k):
    return (X[1],ax(X[1],t,Z[1],k))
def Fz(Z,X,t,k):
    return (Z[1],az(Z[1],t,X[1],k))






# =============================================================================
# Algorithme d'Euler explicite combiner avec la methode des trapéze avec pas h 
# =============================================================================

def euler(f,u,vx0,vz0,x0,z0,t0,h,za,amelioration):
    #methode d'Euler  qui calcule 2 integrale en même temps
    k = 0
    #initialisation (condition initial et déclaration de variable/list)
    t = t0

    lt = [t0]
    
    vx ,vz = vx0 ,vz0
    lvx = [vx0]
    lvz = [vz0]
    
    x , z = x0 ,z0
    
    lx = [x0]
    lz = [z0]
    a_x , a_z = 0 , 0
    lax = [a_x]
    laz = [a_z]

    var1 = 0
    var2 = 0
    vlim = 5
    t1,t2 = 0,0
    while z > 0:
        if z <= za: #si z < za alors le parachute doit être ouvert 
            if amelioration :
                k = 2
            else:
                k = 1
            if var1 == 0:
                var1 = 1
                t1 = t  #temps a laquelle le parachute est ouvert
        else:
            k = 0
        
        if vlim*(1 - 5/100) <= -vz <= vlim*(1 + 5/100) and var2 == 0:
            t2 = t  #temps a partir duquel la période transitoire se termine  
            var2 = 1
        if -vz < vlim*(1 - 5/100) or -vz >  vlim*(1 + 5/100):
            var2 = 0

            
        #si amélioration = True , calcule de la résistance du parachute pendant son temps d'ouverture 
        if amelioration  and z <= za and t <= t1 + t_ouv:
            B[2] = B[1]*np.exp(1/t_ouv*np.log(B[1]/B[0])*((t-t1)-t_ouv))
        if amelioration  and t1 + t_ouv <= t and z <= za :
                k = 1

        a_x , a_z = ax(vx,t,vz,k) , az(vz,t,vx,k)    #calcule de l'accélération  en x en en z
        vx,vz = vx + h*f(vx,t,vz,k),vz+h*u(vz,t,vx,k)#calcule de la vitesse avec la methode d'Euler 
        x += (lvx[-1]+vx)*h/2   #calcule de la position en x avec la methode des trapeze 
        z += (lvz[-1]+vz)*h/2   #calcule de la position en z avec la methode des trapeze
        t += h                  #incrément du temps


        #ajout des valeur a des liste 
        lt.append(t)
        lvx.append(vx)
        lvz.append(vz)
        lx.append(x)
        lz.append(z)
        lax.append(a_x)
        laz.append(a_z)

    return (lt,lvx,lvz,lx,lz,lax,laz,t2,t1)

# =============================================================================
# Algorithme d'Euler explicite avec pas h
# =============================================================================

def eulerbis(f,u,vx0,vz0,x0,z0,t0,h,za,amelioration):
    
    k = 0
    
    #initialisation (condition initial et déclaration de variable/list)
    t = t0

    lt = [t0]
    
    vx ,vz = vx0 ,vz0
    lvx = [vx0]
    lvz = [vz0]
    
    x , z = x0 ,z0
    X,Z = (x,vx),(z,vz)
    lx = [x0]
    lz = [z0]
    a_x , a_z = 0 , 0
    lax = [a_x]
    laz = [a_z]

    var1 = 0
    var2 = 0
    vlim = 5
    t1,t2 = 0,0
    
    while z > 0 :
        if z <= za:
            k = 1
        Ax , Az = ax(vx,t,vz,k) , az(vz,t,vx,k)
        X,Z = [X[0]+h*Fx(X,Z,t,k)[0],X[1]+h*Fx(X,Z,t,k)[1]],[Z[0]+h*Fz(Z,X,t,k)[0],Z[1]+h*Fz(Z,X,t,k)[1]]
        (x,vx) = X
        (z,vz) = Z

        t += h

        lt.append(t)
        lvx.append(vx)
        lvz.append(vz)
        lx.append(x)
        lz.append(z)
        lax.append(Ax)
        laz.append(Az)

    return (lt,lvx,lvz,lx,lz,lax,laz)
    




def chute(x0,z0,vx0,vz0,t0,h,za,f,amelioration):
    #programe claculant d'abort la vitesse et la position du parachutiste
    if not(f):
        B[0]=0
    (lt,lvx,lvz,lx,lz,lax,laz,t2,t1)  = euler(ax,az,vx0,vz0,x0,z0,t0,h,za,amelioration)
    
    T = [lt,lx,lz,lvx,lvz,lax,laz,t2,t1]
    Tc = np.array([[] for k in range(len(lt))])
    for i in T:
        if type(i) == list: #on vérifie que l'élément est bien une list  
            i = np.array(i)
            i = i[:,np.newaxis]
            Tc = np.concatenate((Tc,i),axis=1)  #création d'une matrice contenant toute les valeur de vitesse , position et  accélération  
    return (Tc,t2,t1)


def chuteb(x0,z0,vx0,vz0,t0,h,za,amelioration):
    (ltb,lvxb,lvzb,lxb,lzb,laxb,lazb)  = eulerbis(ax,az,vx0,vz0,x0,z0,t0,h,za,amelioration)
    Tb = [ltb,lxb,lzb,lvxb,lvzb,laxb,lazb]
    Tcb = np.array([[] for k in range(len(ltb))])
    for i in Tb:
        if type(i) == list: #on vérifie que l'élément est bien une list  
            i = np.array(i)
            i = i[:,np.newaxis]
            Tcb = np.concatenate((Tcb,i),axis=1)
    return Tcb



# =============================================================================
# Tracer des courbe 
# =============================================================================

def draw(za = 0,h = 0.01,amelioration = False):
    #amelioration : parmet d'ameliorer la modelisation
    #f : activer les frottement : True
    (T,t2,t1) = chute(0,4000,40,0,0,h,za,True,amelioration)
    (Tb,t2b,t1b) = chute(0,4000,40,0,0,h,za,False,amelioration)
    taille = 10
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)
    plt.rcParams.update({'font.size': 7})
    B[0] = 0.245
    plt.figure('trajectoire de phase')
    plt.suptitle('trajectoire de phase')
    plt.subplot(311)
    plt.title('vx = f(x)', fontsize=taille)
    plt.xlabel('x(m)')
    plt.ylabel('vx(m/s)')
    plt.plot(T[:,1],T[:,3],'--b')
    plt.subplot(212)
    plt.title('vz = f(z)', fontsize=taille)
    plt.xlabel('z(m)')
    plt.ylabel('vz(m/s)')
    plt.plot(T[:,2],T[:,4],'--b')
    for k in range(0,len(T[:,2]),int(200)):
        plt.subplot(311)
        plt.plot(T[k,1],T[k,3],'.b')
        plt.subplot(212)
        plt.plot(T[k,2],T[k,4],'.b')
    
    plt.figure('vitesse')
    plt.suptitle('vitesse')
    plt.subplot(221)
    plt.title('vx = f(t)', fontsize=taille)
    plt.xlabel('t(s)')
    plt.ylabel('vx')
    plt.plot(T[:,0],T[:,3],'--') 
    plt.subplot(222)
    plt.title('vz = f(t)', fontsize=taille)
    plt.xlabel('t(s)')
    plt.ylabel('vz(m/s)')
    plt.plot(T[:,0],T[:,4],'--')
    plt.subplot(212)
    plt.title('v = f(t)', fontsize=taille)
    plt.xlabel('t(s)')
    plt.ylabel('v(m/s)')
    plt.plot(T[:,0],np.sqrt(T[:,4]**2+T[:,3]**2),'-.')

    plt.figure('position')
    plt.suptitle('position')
    plt.subplot(121)
    plt.title('x = f(t)', fontsize=taille)
    plt.xlabel('t(s)')
    plt.ylabel('x(m)')
    plt.plot(T[:,0],T[:,1],'--')
    plt.subplot(122)
    plt.title('z = f(t)', fontsize=taille)
    plt.xlabel('t(s)')
    plt.ylabel('z(m)')
    plt.plot(T[:,0],T[:,2],'--')
    plt.figure('trajectoire')
    plt.suptitle('trajectoire')
    plt.title('z = f(x)', fontsize=9)
    plt.xlabel('x(m)')
    plt.ylabel('z(m)')
    plt.plot(T[:,1],T[:,2],'--r',label=r'avec les frottement')#z =f(x) avec frottement
    plt.plot(Tb[:,1],Tb[:,2],'--b',label=r'sans les frottement')#z =f(x) sans frottement
    
     # affichage: temps de chute/ distance parcourus en x/ valeur moyenne de l'accélération subit 
    print('ouverture du parachute a 1500 m')
    (T,t2,t1) = chute(0,4000,40,0,0,h,1500,True,amelioration)
    print(T[-1,0],'temps de chute en s')
    print(T[-1,1],'distance parcourus sur Ux en m')
    print(t2-t1 , 'temps de transition')
    moyenne = 0
    #calcule de l'acceleration moyenne
    compteur = 0
    index1 = T[:,0].tolist().index(t1)
    index2 = T[:,0].tolist().index(t2)
    for i in range(index1,index2+1): #calcule de l'accélération moyenne subit
        moyenne += np.sqrt(T[i,-1]**2 + T[i,-2]**2)
        compteur += 1
    ##print(max(np.sqrt(T[:,-1]**2+T[:,-2]**2))) #valeur maximal de g subit
    moyenne = moyenne/compteur
    print(moyenne/9.81,'acceleration moyenne subit par le parachutiste en g')
    plt.show()





def comp(x0 = 0,z0 = 4000,vx0 = 40,vz0 = 0,t0 = 0,h = 0.01,za = 1000,amelioration = False):
    #comparaison entre euler et eulerbis
    (T,t2,t1) = chute(0,4000,40,0,0,h,za,amelioration)
    Tb = chuteb(0,4000,40,0,0,h,za,amelioration)
    plt.figure('1')
    plt.title('y = f(x)')
    plt.plot(T[:,3],T[:,4],'g')
    plt.plot(Tb[:,3],Tb[:,4],'b')
    plt.figure('2')
    plt.subplot(211)
    plt.title('vx = f(t)')
    plt.plot(T[:,0],T[:,1],'.--') # vx = f(t)
    plt.plot(Tb[:,0],Tb[:,1],'.--') # vx = f(t)
    plt.subplot(212)
    plt.title('vz = f(t)')
    plt.plot(T[:,0],T[:,2],'.--')#vz = f(t)
    plt.plot(Tb[:,0],Tb[:,2],'.--')#vz = f(t)
    plt.figure('3')
    plt.title('v = f(t)')
    plt.plot(T[:,0],np.sqrt(T[:,2]**2+T[:,1]**2),'.-')#v = f(t)
    plt.plot(Tb[:,0],np.sqrt(Tb[:,2]**2+Tb[:,1]**2),'.-')#v = f(t)
    plt.show()
# =============================================================================
# animation de la chute du parachutiste 
# =============================================================================

def anim(za = 0,h = 0.01,fo = 10,f = True,amelioration = False):
    #fo: vitesse x fo / f: frottement = True - sans frottement = False
    (T,t2,t1) = chute(0,Z_a,40,0,0,h,za,f,amelioration)
    t = 0
    plt.figure('z = f(x)')
    for i in range(int(len(T[:,0])/fo)):
        plt.plot(T[i*fo,3],T[i*fo,4],'.g')
        plt.plot([T[i*fo,3],(T[i*fo,3]+T[i*fo,-1]*10)],[T[i*fo,4],(T[i*fo,4]+T[i*fo,-2]*10)],'r')
        plt.plot([T[i*fo,3],(T[i*fo,3]+T[i*fo,1]*2)],[T[i*fo,4],(T[i*fo,4]+T[i*fo,2]*2)],'b')
        plt.pause(h)
        t += h
        plt.clf()
        plt.ylim(0,Z_a*(1+0.1))
        plt.xlim(0,380)
        plt.title('z=f(x)')
    plt.plot(T[:,3],T[:,4],'--')
    plt.show()


draw()

from numpy import array,float64
import tkinter
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from grav_lib import *
#Objet = [ X, Y, Vitesse_X, Vitesse_Y,Acceleration_X, Acceleration_Y,  masse , radius, id]
#Object_list = [Object_1,Object_2,....]

#--------------------------------------------Constante
dt = 60*60                  #s (pas)
t_fin = 12*2592000      #1 ans
Nb_point = 400



#----------------------------------------------Calcule:
plt.ion()

def Main():
   Menu.destroy()

   Object_list_precedante = Object_list
   record = [[]]
   etape = 0

   t = 0
   capt = 0
   capt_pos = [0 for i in Object_list]
   Nb_iter_tot = t_fin/dt 
   iter_capt = int(Nb_iter_tot/Nb_point)

   iter_compt = 0
   for k in range(len(Object_list)):
      capt_pos[k] = Object_list[k][0:2]
      plt.plot(Object_list[k][0],Object_list[k][1],'.')
   while t < t_fin:

      t += dt
      Object_list_precedante = Object_list
      capt +=1
      iter_compt += 1 
      for k in range(len(Object_list)):
         Object = array(Object_list_precedante[k],dtype =float64)
         Acceleration_precedente = array(Object[4:6])

         Acceleration = PFD(Object, Object_list)
         Vitesse_precedente = array(Object[2:4],dtype = float64)
         V = Vitesse(Object, Acceleration, Acceleration_precedente,dt)
         Position = position(Object, Acceleration_precedente, Vitesse_precedente,dt)


         if capt == iter_capt and 0:
            plt.plot([capt_pos[k][0], Position[0]],[capt_pos[k][1], Position[1]],'--',color = Couleur[int(Object[-1])])
            capt_pos[k] = Position
            record[etape].append([Position[0],Position[1],Object[-2],Object[-1]])

         Object_list[k] = [Position[0], Position[1], V[0], V[1], Acceleration[0], Acceleration[1], Object_list[k][-3], Object_list[k][-2], Object_list[k][-1]]

      if capt == iter_capt:
         record.append([])
         etape += 1
         prog = int(iter_compt/Nb_iter_tot *1000)/10
         print(prog,"%")
         capt = 0
   plt.show()
   #animation(record)
   return


#----------------------------------------------Affichage : 

def animation(rec):
   plt.figure(2)
   fig, ax = plt.subplots()
   for etape in rec:
      ax = plt.gca()
      ax.set_xlim(-170000000000,170000000000)
      ax.set_ylim(-170000000000,170000000000)
      for Object in etape:
         circle32 = Circle((Object[0],Object[1]),Object[-2]*2,color = Couleur[int(Object[-1])])
         ax.add_patch(circle32)
         plt.plot(Object[0],Object[1],'+',color = Couleur[int(Object[-1])])
      plt.pause(1)
      plt.clf()
   plt.show()

      
   plt.pause(0.5)
   fig.savefig('plotcircles2.png')
   plt.show()
   recommencer = input('recommencer?')
   if recommencer:
      animation(rec)
   return


   


#----------------------------------------------Création Objet + Interface :


def Create_Object():
   screen = tkinter.Tk()
   X_pos = tkinter.StringVar(screen)
   Y_pos = tkinter.StringVar(screen)
   
   entry_X = tkinter.Entry(screen, textvariable=X_pos)
   entry_Y = tkinter.Entry(screen, textvariable=Y_pos)
   tkinter.Label(screen, text = '  ').grid(row = 0, column = 0)
   tkinter.Label(screen, text = '   ').grid(row = 0, column = 2)
   tkinter.Label(screen, text = 'New_Object \n').grid(row = 0, column = 3)
   tkinter.Label(screen, text = ' X coord ').grid(row = 1, column = 1)
   entry_X.grid(row = 2, column = 1)
   tkinter.Label(screen, text = '\n Y coord').grid(row = 4, column = 1)
   entry_Y.grid(row = 5 , column = 1)

   VX = tkinter.StringVar(screen)
   VY = tkinter.StringVar(screen)

   entry_VX = tkinter.Entry(screen, textvariable=VX)
   entry_VY = tkinter.Entry(screen, textvariable=VY)
   tkinter.Label(screen, text = '   ').grid(row = 0, column = 5)
   tkinter.Label(screen, text = ' X speed ').grid(row = 1, column = 3)
   entry_VX.grid(row = 2, column = 3)
   tkinter.Label(screen, text = '\n Y speed').grid(row = 4, column = 3)
   entry_VY.grid(row = 5 , column = 3)

   Masse = tkinter.StringVar(screen)
   Radius = tkinter.StringVar(screen)
   entry_Masse = tkinter.Entry(screen, textvariable = Masse)
   entry_Radius = tkinter.Entry(screen, textvariable = Radius)
   tkinter.Label(screen, text = '   ').grid(row = 0, column = 6)
   tkinter.Label(screen, text = '   ').grid(row = 0, column = 4)
   tkinter.Label(screen, text = ' Masse ').grid(row =1, column = 5)
   entry_Masse.grid(row = 2, column = 5)
   tkinter.Label(screen, text = '  Radius').grid(row = 4, column = 5)
   entry_Radius.grid(row = 5 , column = 5)


   def get_var():
      screen.destroy()
      X = X_pos.get()
      Y = Y_pos.get()
      V_X = VX.get()
      V_Y = VY.get()
      M = Masse.get()
      R = Radius.get()
      Object = [float(X), float(Y), float(V_X), float(V_Y), 0, 0, 0, float(M), float(R), len(Object_list) +1 ]
      Object_list.append(Object)
      


   bouton = tkinter.Button(screen, text = 'create', command = get_var)
   bouton.grid(row = 10 ,column = 3)

   screen.mainloop()
   return
#----------------------------------------------Menu:
def setting():
   sett = tkinter.Tk()
   fen = tkinter.LabelFrame(sett, text = "setting",padx = 20,pady = 20)
   fen.pack()
   tkinter.Label(fen, text = "  dt (10^?):  ").pack()
   log_dt = tkinter.Spinbox(fen, from_ = -3 , to=1)
   log_dt.pack()

   tkinter.Label(fen,text = 'end time ( = 5 ) : ').pack()
   entry = tkinter.Entry(fen,bd = 5)
   entry.pack()

   def get_dt():
      global dt
      global t_fin
      dt = 10 ** int(log_dt.get())
      t_fin = int(entry.get())
      sett.destroy()
   tkinter.Button(fen, text = "confirm", command = get_dt).pack()
   sett.mainloop()
   return


Couleur = [None,'yellow','deepskyblue','darkgrey']
def Menu():
   global Object_list
   global Menu
   sys_sol = True
   Object_list = []
   Object_list.append([0,0,0,0,0,0,2000000000000000000000000000000,695510000,1])
   Object_list.append([150000000000,0,0,29778,0,0,6000000000000000000000000,6371000,2])
   Object_list.append([150000000000,-384400000,1022,29778,0,0,70000000000000000000000,1737100,3])
   Object_list.append([-58000000000,0,0,-47900,0,0,330110000000000000000000,1,4])
   Menu = tkinter.Tk()
   tkinter.Label(Menu, text = '   Menu   ').pack()
   New_Object = tkinter.Button(Menu, text = 'Create new object', command = Create_Object)
   sim = tkinter.Button(Menu, text = 'simulate',command = Main)  # lancer la simulation
   setting_button = tkinter.Button(Menu, text = 'setting', command = setting )
   Fermer = tkinter.Button(Menu, text = 'Fermer', command = Menu.destroy)
   sim.pack()
   New_Object.pack()
   setting_button.pack()
   Fermer.pack()


   Menu.mainloop()
   return

Menu()

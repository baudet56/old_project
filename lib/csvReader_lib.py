





def lecture(nom_fichier,nb_colone = 2):
    fichier = open(nom_fichier,'r')
    lignes = fichier.readlines()
    donnée = [[] for i in range(nb_colone)]
    for ligne in lignes:
        ligne = ligne.strip('\n')
        if ligne != '':
            valeur = ligne.split(';')
            for k in range(nb_colone):
                donnée[k] += [float(valeur[k])]
    fichier.close()
    return (donnée)

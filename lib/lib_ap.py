


def approximation(nombre,precision = 2):
    #precision: nombre de chifre apres la virgule (2  de base)
    n = int(nombre * 10**precision)
    e = nombre * 10**(precision+1) - n * 10
    if e >= 5:
        n += 1
    elif -e >= 5:
        n -= 1
    return n / 10**(precision)


def liste_ap(Liste,precision = 2):
    #precision: nombre de chifre apres la virgule (2  de base)
    ap = []
    for i in range(len(Liste)):
        ap += [approximation(Liste[i],precision)]
    return ap
        
        



def matrice_ap(Matrice,precision = 2):
    #precision: nombre de chifre apres la virgule (2  de base)
    ap = []
    for i in Matrice:
        ap += liste_ap(i)
    return ap

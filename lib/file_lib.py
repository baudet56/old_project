

def write(name,doc,mode = 'w'):
    """
    mode :
     -'w': create or replace a data base
     -'a': add new data into the data base
     """
    f = open( name, mode)
    doc_type = type( doc)
    
    if type(doc) == list:
        dim = detect_dim( doc)
        write_liste( f, doc, dim)
    else:
        f.write(str(doc)+'\n')
    f.close()
 
def detect_dim(doc):
    a = doc[0]
    doc_type = type(a)
    if doc_type == int or doc_type == float or doc_type == str:
         return 1
    return detect_dim(a) + 1 


    
def tab_r(name,sep = ";", read_first_ligne = True):
    """
    name : name.txt(.csv ...)
    dim: number of col
    sep: separator (";")
    """
    f = open(name,'r')
    if not(read_first_lignefirstl):
        f.readline()
    lignes = f.readlines()
    dim = len(lignes)
    donnée = [[] for i in range(dim)]
    for ligne in lignes:
        ligne = ligne.strip('\n')
        if ligne != '':
            valeur = ligne.split(sep)
            for k in range(dim):
                donnée[k] += [float(valeur[k])]
    f.close()
    return donnée

def list_w(name,doc,mode = 'w',sep =';'):
    """ liste must contain float or int """ 
    f = open(name,mode)
    dim = len(doc)
    af = ''
    for k in doc:
        af += str(k)+sep
    af = af.strip(sep)
    af += '\n'
    f.write(af)
    f.close()
     
    
    

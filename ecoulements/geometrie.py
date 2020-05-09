import numpy as np

#numbering a matrix (the geometry matrix)
def numeroter(matriceGeometrie):
    matriceNum = np.copy(matriceGeometrie)
    
    i=1
    for item in np.nditer(matriceNum, op_flags=['readwrite']):
        if item in [1,2,3]:
            item[...] = i
            i += 1
    
    matriceNum = matriceNum.astype(int)
    return matriceNum #returns the numbered matrix 

#counting the number of fluid cells
def numCases(matriceGeometrie):
    i = 0
    for item in np.nditer(matriceGeometrie):
        if item in [1,2,3]:
            i += 1
            
    return i

#table with all the coordinates of the numbered elements
def tableaucoord(matriceGeometrie, matriceNumerotee, nomCases):
    tableauliste = [0]
    
    for num in range(1, nomCases+1):
        i,j = np.where(matriceNumerotee==num)
        i,j = int(i), int(j)
        tableauliste.append([i,j])
        
    return tableauliste
    
    

#neighborhood of an element, returns a dictionary with the value of the neighboors, to be used with a numbered matrix
def voisinage(matrice, i,j): #i,j: coordinates of the element that we are looking at 
    voisins = {} #dictionary for the neighboors, left, right, up and down
    numvoisins = 0
    #up voisin
    if (i-1)>=0 and matrice[i-1, j]!=0:
        voisins['up'] = matrice[i-1,j]
        numvoisins += 1
        
    #down voisin
    if (i+1)<np.shape(matrice)[0] and matrice[i+1,j]!=0 :
        voisins['down'] = matrice[i+1,j]
        numvoisins += 1
        
    #left voisin
    if (j-1)>=0 and matrice[i, j-1]!=0 :
        voisins['left'] = matrice[i, j-1]
        numvoisins += 1
        
    #right voisin
    if (j+1)<np.shape(matrice)[1] and matrice[i, j+1]!=0 :
        voisins['right'] = matrice[i, j+1]
        numvoisins += 1
        
    return voisins, numvoisins

#fonctions to know if the element is in a border
#be careful not to write coordinates bigger than the dimensions of the matrix

#vertical axis
def estBordv(matrice, i, j, shape=None):
    if shape==None:
        shape = np.shape(matrice)
    
    if i == 0 :
        positionv = 'up'
    elif i == shape[0]-1 :
        positionv = 'down'
    elif 0<i<shape[0]-1 :
        positionv = 'inside'
        
    return positionv

#horizontal axis
def estBordh(matrice, i, j, shape=None):
    if shape==None:
        shape = np.shape(matrice)
    
    if j==0:
        positionh = 'left'
    elif j== shape[1]-1:
        positionh = 'right'
    elif 0<j<shape[1]-1:
        positionh = 'inside'
        
    return positionh

#both axis
def estBord(matrice, i, j): #matrix and element that we check
    
    positionh = estBordh(matrice, i, j)
    positionv = estBordv(matrice, i, j)
        
    return [positionh, positionv]

#looking for neighbooring NaN values, to see NaN values as a border:

#vertical axis
def estBordv_nan(matrice, i,j, shape=None):
    if shape == None:
        shape = matrice.shape
        
    positionv = estBordv(matrice, i,j, shape=shape) 
    
    if positionv == 'up':
        if np.isnan(matrice[i+1,j]):
            positionv = 'isolated'
    
    if positionv == 'down':
        if np.isnan(matrice[i-1,j]):
            positionv = 'isolated'
    
    if positionv == 'inside':
        if np.isnan(matrice[i+1,j]) and np.isnan(matrice[i-1,j]):
            positionv = 'isolated'
        elif np.isnan(matrice[i+1,j]):
            positionv = 'down'
        elif np.isnan(matrice[i-1,j]):
            positionv = 'up'
    
    return positionv

#horizontal axis
def estBordh_nan(matrice, i,j, shape=None):
    if shape == None:
        shape = matrice.shape
        
    positionh = estBordh(matrice, i,j, shape=shape) 
    
    if positionh == 'left':
        if np.isnan(matrice[i,j+1]):
            positionh = 'isolated'
    
    if positionh == 'right':
        if np.isnan(matrice[i,j-1]):
            positionh = 'isolated'
    
    if positionh == 'inside':
        if np.isnan(matrice[i,j+1]) and np.isnan(matrice[i,j-1]):
            positionh = 'isolated'
        elif np.isnan(matrice[i,j+1]):
            positionh = 'right'
        elif np.isnan(matrice[i,j-1]):
            positionh = 'left'
    
    return positionh
        
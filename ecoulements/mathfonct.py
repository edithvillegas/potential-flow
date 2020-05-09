import numpy as np
from ecoulements import geometrie 


#gradient: (i,j) element of the matrix gradient of a matrix, y component
def gradiently(matrice, i,j, h=1, t='progressive'):
    if t == 'progressive':
        gradly = (matrice[i+1,j] - matrice[i,j])/h
        
    if t == 'retrograde':
        gradly = (matrice[i,j] - matrice[i-1,j])/h
        
    if t == 'centree' :
        gradly = (matrice[i+1,j]-matrice[i-1,j])/(2*h)
        
    return gradly 

#gradient: x component,  element(i,j)
def gradientlx(matrice, i,j, h=1, t='progressive'):
    if t == 'progressive':
        gradlx = (matrice[i,j+1] - matrice[i,j])/h
        
    if t == 'retrograde':
        gradlx = (matrice[i,j] - matrice[i,j-1])/h
        
    if t == 'centree' :
        gradlx = (matrice[i,j+1]-matrice[i,j-1])/(2*h)
        
    return gradlx

#complete y component of the gradient
def gradienty(matrice, h=1):
    shape = matrice.shape
    gradienty = np.zeros(shape)
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            
            if i == 0:
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='progressive')
            elif i == shape[0]-1 :
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='retrograde')
            else:
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='centree')

    return gradienty

#complete x component of the gradient
def gradientx(matrice, h=1):
    shape = matrice.shape
    gradientx = np.zeros(shape)
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            
            if j == 0:
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='progressive')
            elif j == shape[1]-1:
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='retrograde')
            else:
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='centree')
                
    return gradientx



#-------------------------------------------------------------------
# y component of the gradient that works around NaNs
def gradienty_c(matrice, h=1):
    shape = matrice.shape
    gradienty = np.zeros(shape)
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            
            positionv = geometrie.estBordv_nan(matrice, i,j, shape=shape)
            
            if positionv == 'up' :
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='progressive')
            elif positionv == 'down':
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='retrograde')
            elif positionv == 'inside':
                gradienty[i,j] = gradiently(matrice, i,j, h=h, t='centree')
            elif positionv == 'isolated':
                gradienty[i,j]= 0
                
            if np.isnan(matrice[i,j]):
                gradienty[i,j] = float('nan')
                
                
    return gradienty

#x component of the corrected gradient that works around NaNs
def gradientx_c(matrice, h=1):
    shape = matrice.shape
    gradientx = np.zeros(shape)
    
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            
            positionh = geometrie.estBordh_nan(matrice, i,j, shape=shape)
            
            if positionh == 'left':
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='progressive')
            elif positionh == 'right':
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='retrograde')
            elif positionh == 'inside':
                gradientx[i,j] = gradientlx(matrice, i,j, h=h, t='centree')
            elif positionh == 'isolated':
                gradientx[i,j] = 0
                
            if np.isnan(matrice[i,j]):
                gradientx[i,j] = float('nan')
                
    return gradientx

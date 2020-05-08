# -*- coding: utf-8 -*-
"""
Created on Fri May  8 22:25:41 2020

@author: Administrador
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

import systeme
import affichages 

#READ THE IMAGE 
file_name = "pics/smile.bmp" #or "person.bmp"
matrix = misc.imread(file_name) #reads the file
matrix = matrix[:,:,1] #retains only one color channel
shape = np.shape(matrix) #save shape of the matrix

#changing white cells to fluid cells with value 2
for i in range(shape[0]):
    for j in range(shape[1]):
        if matrix[i,j]==255: #white pixels with maximum value
            matrix[i,j]= 1 #are changed to fluid cells (2)
            
#addd entry and exit cells 
for i in range(shape[1]):
    matrix[0,i] = 2 #entry 
    matrix[shape[0]-1, i]= 3 #exit 
    
plt.imshow(matrix)
plt.colorbar()

#CHANGING THE DATA TYPE (originally dtyp-uint8 can only store up to 255 )
matrix = np.array(matrix, dtype='int32')


#CALCULATING THE FLOW
#initial conditions 
h=1
v=1
phiref=1
p0=1
rho=1
ht = 1

#calculation
phi, VX, VY, P = systeme.sol(matrix, h=h, v=v, phiref=phiref, p0=p0, rho=rho)

nom = file_name

affichages.affPotentiel(phi, matrix, nom=nom)
affichages.affVitesse(VX, VY, matrix, nom=nom)
affichages.affCourant(VX, VY, matrix, nom=nom) 
            

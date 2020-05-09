# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 10:09:59 2018

@author: EV
"""
import numpy as np
from scipy import interpolate
from ecoulements import geometrie

#function to convert the NaNs in a matrix to zeros
def nantozero(matrice):
    matrice_c = np.nan_to_num(matrice)              
    return matrice_c

#function to get the functions that interpolate vx and vy
def interpolation(vx,vy, kind='linear'):
    shape = vx.shape
    x = np.linspace(0,shape[1]-1, shape[1])
    y = np.linspace(0, shape[0]-1, shape[0])
    fvx = interpolate.interp2d(x, y, vx, kind=kind)
    shape = vy.shape
    x = np.linspace(0,shape[1]-1, shape[1])
    y = np.linspace(0, shape[0]-1, shape[0])
    fvy = interpolate.interp2d(x, y, vy, kind=kind)
    return fvx, fvy

#function to get the trajectory of a particle in the fluid (Euler's Method)
def trajectoirelim(x0, y0, fvx, fvy, lim, typelim, tcoord, maxit=2000, ht=1):    
    #initial conditions
    x = [x0]
    y = [y0]
    x_nmoins1 = x0
    y_nmoins1 = y0
    compteur = 0
    
    while(compteur<maxit):
        vx = fvx(x_nmoins1, y_nmoins1)
        vy = fvy(x_nmoins1, y_nmoins1)
        x_n = x_nmoins1 + ht*vx
        y_n = y_nmoins1 + ht*vy
        x.append(x_n)
        y.append(y_n)
        x_nmoins1 = x_n
        y_nmoins1 = y_n  
        
        compteur +=1
        
        #breaking conditions
        ymax_reached = typelim=='ymax' and y_nmoins1>lim
        ymin_reached = typelim=='ymin' and y_nmoins1<lim
        xmax_reached = typelim=='xmax' and x_nmoins1>lim
        xmin_reached = typelim=='xmin' and x_nmoins1<lim
        if xmax_reached or xmin_reached or ymax_reached or ymin_reached:
            break
        
        #if the particule hits an obstacle
        if [round(float(y_n)), round(float(x_n))] not in tcoord:
            break
        
    return x,y

#function to get the trajectory of a particle in the fluid (RK4 Method)
def trajectoireRK4(x0, y0, fvx, fvy, lim, typelim, tcoord, maxit=2000, ht=1):
    #initial conditions
    x = [x0]
    y = [y0]
    x_nmoins1 = x0
    y_nmoins1 = y0
    compteur = 0
    
    while(compteur<maxit):
        #k1
        k1x = fvx(x_nmoins1, y_nmoins1)
        k1y = fvy(x_nmoins1, y_nmoins1)
        
        #k2
        x_demi = x_nmoins1 + (ht/2)*k1x
        y_demi = y_nmoins1 + (ht/2)*k1y
        k2x = fvx(x_demi, y_demi)
        k2y = fvy(x_demi, y_demi)
        
        #k3
        x_demi = x_nmoins1 + (ht/2)*k2x
        y_demi = y_nmoins1 + (ht/2)*k2y
        k3x = fvx(x_demi, y_demi)
        k3y = fvy(x_demi, y_demi)
        
        #k4
        x_n = x_nmoins1 + ht*k3x
        y_n = y_nmoins1 + ht*k3y
        k4x = fvx(x_n, y_n)
        k4y = fvy(x_n, y_n)
        
        x_n = x_nmoins1 + ht*(1/6)*(k1x+ 2*k2x + 2*k3x + k4x)
        y_n = y_nmoins1 + ht*(1/6)*(k1y+ 2*k2y + 2*k3y + k4y)
        x.append(x_n)
        y.append(y_n)
        x_nmoins1 = x_n
        y_nmoins1 = y_n  
        
        compteur +=1
        
        #breaking conditions
        ymax_reached = typelim=='ymax' and y_nmoins1>lim
        ymin_reached = typelim=='ymin' and y_nmoins1<lim
        xmax_reached = typelim=='xmax' and x_nmoins1>lim
        xmin_reached = typelim=='xmin' and x_nmoins1<lim
        if xmax_reached or xmin_reached or ymax_reached or ymin_reached:
            break
        
        #if the particule hits an obstacle
        if [round(float(y_n)), round(float(x_n))] not in tcoord:
            break
        
    return x,y
    
#function to find the coordinates of the entry and exit
def coord(matriceGeometrie, tcoord, nomCases):
    coordentree = []
    coordsortie = []
    for n in range(1,nomCases+1):
        coord = tcoord[n]
        if matriceGeometrie[coord[0],coord[1]]==2:
            coordentree.append(coord)
        elif matriceGeometrie[coord[0],coord[1]]==3:
            coordsortie.append(coord)
    return coordentree, coordsortie 

#orientation of the entry and exit cells
def orientation(matriceGeometrie, coords):
    coordentree = coords[0]
    coordsortie = coords[1]
    
    coord = coordentree[0]
    positionh, positionv = geometrie.estBord(matriceGeometrie, coord[0],coord[1])
    if positionh == 'left':
        orient_entree = 'vertical, left'
    elif positionh == 'right':
        orient_entree = 'vertical, right'
    elif positionv == 'up':
        orient_entree = 'horizontal, up'
    elif positionv == 'down':
        orient_entree = 'horizontal, down'
    
    coord = coordsortie[0]
    positionh, positionv = geometrie.estBord(matriceGeometrie, coord[0],coord[1])
    if positionh == 'left':
        orient_sortie = 'vertical, left'
    elif positionh == 'right':
        orient_sortie = 'vertical, right'
    elif positionv == 'up':
        orient_sortie = 'horizontal, up'
    elif positionv == 'down':
        orient_sortie = 'horizontal, down'
    
    return orient_entree, orient_sortie


import numpy as np
from ecoulements import mathfonct
from ecoulements.geometrie import *

#function to find B in the matrix equation Ax = B
def systemeB(matriceGeometrie, nomCases, tcoord, h=1, v=1, phiref=1):
    B = np.zeros(nomCases)
    
    for n in range(1, nomCases+1):
        coord = tcoord[n]
        if matriceGeometrie[coord[0],coord[1]]==1:
            pass
        elif matriceGeometrie[coord[0],coord[1]]==2:
            B[n-1] = h*v
        elif matriceGeometrie[coord[0],coord[1]]==3 :
            B[n-1] = phiref
    return B

#function to define the equations for the exit cells
def eqSortie(matriceGeometrie, nomCases, matriceNumerotee, i,j):
    eq = np.zeros(nomCases)
    numPhi = matriceNumerotee[i,j] #number of the unknown phi we are looking at
    
    eq[numPhi-1] = 1 #-1 because arrays begin at 0, while phis begin at 1
    return eq

#function to define the equations for the entry cells
#we give the matrix of the geometry and the coordinates of the entry cell that we want the equation for 
def eqEntree(matriceGeometrie, nomCases, matriceNumerotee, i,j): 
    eq = np.zeros(nomCases) 
    numPhi = matriceNumerotee[i,j] #the number of the unknown phi we are looking at 
    
    eq[numPhi-1] = 1 
    
    #the names are a little bit confusing, because in the booklet i corresponds to the x axis and j to the y axis
    #but here i is the name of the lines, so moving in i (adding or substracting 1) is moving in the y axis
    if estBord(matriceGeometrie,i,j)[0]=='left':
        numPhi_iplus1 = matriceNumerotee[i,j+1]
        eq[numPhi_iplus1-1] = -1
    elif estBord(matriceGeometrie,i,j)[0] == 'right':
        numPhi_imoins1 = matriceNumerotee[i,j-1]
        eq[numPhi_imoins1-1] = -1
    elif estBord(matriceGeometrie,i,j)[1] == 'up':
        numPhi_jplus1 = matriceNumerotee[i+1,j]
        eq[numPhi_jplus1-1] = -1
    elif estBord(matriceGeometrie, i,j)[1] == 'down':
        numPhi_jmoins1 = matriceNumerotee[i-1,j]
        eq[numPhi_jmoins1-1] = -1  
        
    return eq


#function to define the eq for the standard cells
def eqStandard(matriceGeometrie, nomCases, matriceNumerotee, i,j): 
    eq = np.zeros(nomCases)
    numPhi = matriceNumerotee[i,j]
    voisins, numvoisins = voisinage(matriceNumerotee, i,j)
    voisins = list(voisins.values())
    
    eq[numPhi-1] = -1*numvoisins
    
    for voisin in voisins:
        eq[voisin-1] = 1
            
    return eq

#put together all the equations
def systemeA(matriceGeometrie, nomCases, matriceNumerotee, tcoord):
    A = np.zeros((nomCases, nomCases))
    
    for n in range(1, nomCases+1):
        coord = tcoord[n]
        if matriceGeometrie[coord[0],coord[1]]==2:
            A[n-1] = eqEntree(matriceGeometrie, nomCases, matriceNumerotee, coord[0],coord[1])
        elif matriceGeometrie[coord[0],coord[1]]==1:
            A[n-1] = eqStandard(matriceGeometrie, nomCases, matriceNumerotee, coord[0],coord[1])
        elif matriceGeometrie[coord[0],coord[1]]==3:
            A[n-1] = eqSortie(matriceGeometrie, nomCases, matriceNumerotee, coord[0],coord[1])
            
    return A

#returns the matrix with the PHI potential
def PHI(matriceGeometrie, nomCases, matriceNumerotee, tcoord, h=1, v=1, phiref=1):
    A = systemeA(matriceGeometrie, nomCases, matriceNumerotee, tcoord)
    B = systemeB(matriceGeometrie, nomCases, tcoord, h=h, v=v, phiref=phiref)
    phi_array = np.linalg.solve(A,B)
    
    PHI = np.zeros(matriceGeometrie.shape)
    
    for n in range(1,nomCases+1):
        coord = tcoord[n]
        PHI[coord[0],coord[1]] = phi_array[n-1]
    
    return PHI

#to write NaN where the value of the matrix should not be defined (walls, obstacles)
def c_nan(matrice, matriceGeometrie):
    shape = np.shape(matriceGeometrie)
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if matriceGeometrie[i,j] == 0:
                matrice[i,j] = float('nan')
                
    return matrice

#---------------------------------------------------------------------------------------------------------------------------------------
#to find the velocities
def vitesse(phi, h=1):
    
    VX = -1*mathfonct.gradientx_c(phi, h=h)
    VY = -1*mathfonct.gradienty_c(phi, h=h) 
    
    return VX,VY

#to find the pressure
def pression(VX, VY, matriceGeometrie, tcoord=None, p0=1, rho=1, v=1):
    if tcoord == None:
        tcoord = geometrie.tableaucoord(matriceGeometrie)
    
    cte = p0 + 1/2*(rho*v**2)
    
    P = np.zeros(matriceGeometrie.shape)
    num = numCases(matriceGeometrie)
    
    for n in range(1, num+1):
        coord = tcoord[n]
        P[coord[0], coord[1]]= cte - 1/2*(rho*np.sqrt( VX[coord[0],coord[1]]**2+VY[coord[0],coord[1]]**2 ) )
        
    return P

#find, phi, vx, vy, P
def sol(matriceGeometrie, h=1, v=1, phiref=1, p0=1, rho=1):
    matriceNumerotee = numeroter(matriceGeometrie)
    num = numCases(matriceGeometrie)
    tcoord = tableaucoord(matriceGeometrie, matriceNumerotee, num)
    phi = PHI(matriceGeometrie, num, matriceNumerotee, tcoord, h=h, v=v, phiref=phiref)
    phi = c_nan(phi, matriceGeometrie)
    
    vx, vy = vitesse(phi, h=h)
    P = pression(vx, vy, matriceGeometrie, tcoord=tcoord, p0=p0, rho=rho, v=v)
    P = c_nan(P, matriceGeometrie)
    
    return phi, vx, vy, P

#entry and exit velocities
def vEntree(VX,VY, matriceGeometrie, shape=None):
    vin = []
    if shape==None:
        shape = matriceGeometrie.shape
    
    for i in range(0,shape[0]):
        for j in range(0,shape[1]):
            if matriceGeometrie[i,j] == 2:
                vin.append([(i,j), VX[i,j], VY[i,j]])
                            
    return vin
                            
def vSortie(VX,VY, matriceGeometrie, shape=None):
    vout = []
    if shape==None:
        shape = matriceGeometrie.shape
    
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if matriceGeometrie[i,j] == 3:
                vout.append([(i,j), VX[i,j], VY[i,j]])

    return vout

#force on the obstacle
def calculForce(P, numline, lmin, lmax, h=1, horizontal=True):
    if horizontal:
        Pp = P[numline, lmin:(lmax+1):1]
    else:
        Pp = P[lmin:(lmax+1):1, numline]
        
    force = np.trapz(Pp, dx=h)
    return force

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 12:16:20 2018

@author: E Villegas
"""

import defGeometrie
import systeme
import affichages

#defining the initial parameters: 
print("Conditions Initiales")
v = float(input("Ecrivez la vitesse initale du fluide "))
phiref = float(input("Ecrivez la valeur de reference pour le potentiel de vitesses "))
p0 = float(input("Ecrivez la valeur initale de la pression "))
rho= float(input("Ecrivez la valeur de la densite du fluide "))
h = float(input("Ecrivez la taille du pas de la grille "))
ht = float(input("Ecrivez la taille du pas dans le temps "))
print("Ecrivez les dimensions de la matrice")
pointsx = int(input("x: "))
pointsy = int(input("y: "))

#defining the geometry
print("")
print("Geometrie")
print("Ecrivez le type de geometrie (1:canal simple, 2:canal avec elargissement, 3:canal avec coude, 4: canal avec obstacle)")
typegeometrie = int(input())

if typegeometrie == 1:
    print("Canal Rectiligne Simple")
    nom = 'Canal Simple'
    geometry = defGeometrie.canalh(pointsx, pointsy)

elif typegeometrie == 2:
    print("Canal avec elargissement")
    nom = 'Canal Elargissement'
    l0 = int(input("Ecrivez la hauteur initiale du canal "))
    lf = int(input("Ecrivez la hauteur finale du canal "))
    geometry = defGeometrie.canalElargi(pointsx, pointsy, l0, lf)

elif typegeometrie == 3:
    print("Canal avec un coude")
    nom = 'Canal avec Coude'
    coudex = int(input("Ecrivez la largeur du coude "))
    coudey = int(input("Ecrivez la hauteur du coude "))
    geometry = defGeometrie.canalCoude(pointsx, pointsy, coudex, coudey)
    
elif typegeometrie == 4:
    print("Canal avec obstacle")
    nom = 'Canal Obstacle'
    print("Ecrivez la position de l'obstacle")
    x0 = int(input("position x du coin en haut a gauche "))
    y0 = int(input("position y du coin en haut a gauche "))
    xf = int(input("position x du coin en bas a droite "))
    yf = int(input("position y du coin en bas a droite "))
    geometry = defGeometrie.canalObstacle(pointsx, pointsy, x0, y0, xf, yf)

#solving and showing common results
phi, VX, VY, P = systeme.sol(geometry, h=h, v=v, phiref=phiref, p0=p0, rho=rho)

vin = systeme.vEntree(VX.round(2), VY.round(2), geometry)
vout = systeme.vSortie(VX.round(2), VY.round(2), geometry)

print("Vitesses Initiales: (x,y) vx, vy")
print(vin)
print("Vitesses Finales: (x,y), vx, vy ")
print(vout)

affichages.affPotentiel(phi, geometry, nom=nom)
affichages.affPression(P.round(2), geometry, nom=nom)
affichages.affCourant2(VX, VY, geometry, ht=ht, nom=nom) 

if typegeometrie in [1,2,4]:
    affichages.affVitesse(VX, VY, geometry, numval = True, vin=vin, vout=vout, nom=nom)
elif typegeometrie == 3:
    affichages.affVitesse(VX, VY, geometry, numval = True, vin=vin, vout=vout, nom=nom, textrotation=90)

#speed profiles, pressure and force on the obstacle
if typegeometrie == 2:
    #speed profile
    affichages.ProfilVitesse(VX, VY, 0, horizontal=False, nom=nom+' (entree)')
    affichages.ProfilVitesse(VX, VY, pointsx-1, horizontal=False, nom=nom+' (sortie)')
    
elif typegeometrie == 3:
    #speed profile
    affichages.ProfilVitesse(VX, VY, coudex-1, horizontal=False, nom=nom+' (avant obstacle)')
    affichages.ProfilVitesse(VX, VY, coudey-1, nom=nom+' (apres obstacle)')
    
    #force and pressure on the deviator
    affichages.TracePression(P, coudey, 0, coudex, horizontal=True, nom=nom)
    force = systeme.calculForce(P,coudey, 0, coudex, h=h, horizontal=True)
    print("La force sur l'obstacle est de {}".format(force))

elif typegeometrie == 4:
    #speed profiles
    affichages.ProfilVitesse(VX, VY, x0-1, horizontal=False, nom=nom+' (avant obstacle)')
    affichages.ProfilVitesse(VX, VY, xf+1, horizontal=False, nom=nom+' (apres obstacle)')
    
    #force and pressure on the obstacle
    affichages.TracePression(P, x0-1, y0, yf, horizontal=False, nom=nom)
    force = systeme.calculForce(P, x0-1,y0, yf, h=h, horizontal=False)
    print("La force sur l'obstacle est de {} ".format(force))
    
#compare Euler's method with Runge-Kutta of order 4 (for h=1 and h=0.1)
print("Voir l'influence de la methode d'integration sur les lignes de courant? (oui ou non)")
rep = input()
ht1 = 0.5
ht2 = 0.1
if rep == 'oui':
    affichages.affCourant2(VX, VY, geometry, ht=ht1, 
                           nom=nom+'(comparaison ht={})'.format(ht1), 
                           methode = 'comparaison')
    affichages.affCourant2(VX, VY, geometry, ht=ht2, 
                           nom=nom+'(comparaison ht={})'.format(ht2),
                           methode = 'comparaison')

    
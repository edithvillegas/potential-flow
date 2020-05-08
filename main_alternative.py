# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 13:55:56 2018

@author: Administrador
"""

import defGeometrie
import systeme
import affichages

#initial conditions 
h=1
v=1
phiref=1
p0=1
rho=1
ht = 1

#circular obstacle
canalcirc = defGeometrie.canalcircle(50,50,25,25,10)
phi, VX, VY, P = systeme.sol(canalcirc, h=h, v=v, phiref=phiref, p0=p0, rho=rho)

nom = 'Obstacle Circulaire'

affichages.affPotentiel(phi, canalcirc, nom=nom)
affichages.affPression(P.round(2), canalcirc, nom=nom)
affichages.affCourant2(VX, VY, canalcirc, ht=ht, nom=nom) 
affichages.affVitesse(VX, VY, canalcirc)

affichages.affCourant2(VX, VY, canalcirc, ht=ht, 
                           nom=nom+'(comparaison ht={})'.format(ht1), 
                           methode = 'comparaison')

#triangular obstacle
canaltri = defGeometrie.canaltriang(50,50,25,25,7)
phi, VX, VY, P = systeme.sol(canaltri, h=h, v=v, phiref=phiref, p0=p0, rho=rho)

nom = 'Obstacle Triangulaire'

affichages.affPotentiel(phi, canaltri, nom=nom)
affichages.affPression(P.round(2), canaltri, nom=nom)
affichages.affCourant2(VX, VY, canaltri, ht=ht, nom=nom) 
affichages.affVitesse(VX, VY, canaltri)

affichages.affCourant2(VX, VY, canaltri, ht=ht, 
                           nom=nom+'(comparaison ht={})'.format(ht1), 
                           methode = 'comparaison')
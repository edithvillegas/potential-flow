
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np 

from ecoulements import integrafonct 
from ecoulements import geometrie

def affGeometrie(matriceGeometrie):
    plt.figure()
    plt.imshow(matriceGeometrie, cmap = 'coolwarm')
    plt.colorbar()
    plt.show()
    
def affPotentiel(phi, matriceGeometrie, nom=''):
    #geometry matrix (background)
    fig = plt.figure()
    fig.suptitle('Potentiel de Vitesses ' r'$\phi $', fontweight='bold')
    sub = fig.add_subplot(111)
    sub.imshow(matriceGeometrie, cmap='coolwarm', origin='lower')
    ax = fig.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    sub.tick_params(axis='both', which='major', labelsize=6) 
    
    #contour plot
    cp = sub.contour(phi)
    sub.clabel(cp)
    fig.colorbar(cp)
    fig.savefig(nom+"-Potentiel Phi.pdf")

    
def affVitesse(VX,VY, matriceGeometrie, numval = False, vin = None, vout = None, nom='', textrotation =0):
    #geometry
    fig = plt.figure()
    fig.suptitle('Champ de Vitesses', fontweight='bold')
    sub = fig.add_subplot(111)
    sub.imshow(matriceGeometrie, cmap='coolwarm', origin='lower')
    ax = fig.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    sub.tick_params(axis='both', which='major', labelsize=6)
    
    #velocity
    sub.quiver(VX,VY)
    
    #writing the numerical values for the initial and final velocity in the plot (if they were given)
    if numval:
        for item in vin:
            i,j = item[0]
            sub.text(j,i, str(item[1])+', '+str(item[2]), horizontalalignment = 'right', verticalalignment='bottom', 
                     fontsize = 6, rotation = 0, bbox={'facecolor':'white', 'alpha':0.5, 'pad':1})
        for item in vout:
            i,j = item[0]
            sub.text(j,i, str(item[1])+', '+str(item[2]), horizontalalignment = 'left', verticalalignment='top', 
                     fontsize = 6, rotation = textrotation, bbox={'facecolor':'white', 'alpha':0.5, 'pad':1})
            
    fig.savefig(nom+"-Champ de Vitesses.pdf")
    
def affCourant(VX, VY, matriceGeometrie, nom=''):
    #geometry
    fig = plt.figure()
    fig.suptitle('Lignes de Courant', fontweight='bold')
    sub = fig.add_subplot(111)
    sub.imshow(matriceGeometrie, cmap='coolwarm', origin='lower')
    ax = fig.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    sub.tick_params(axis='both', which='major', labelsize=6)
    
    #Streamplot
    dim = np.shape(matriceGeometrie)[0]
    x = np.linspace(0,dim-1,dim)
    y = np.linspace(0,dim-1,dim)
    sub.streamplot(x,y,VX,VY)
    
    fig.savefig(nom+"-Lignes de Courant.pdf")
    
def affPression(P, matriceGeometrie, nom=''):
    #geometry
    fig = plt.figure()
    fig.suptitle('Champ de Pression', fontweight='bold')
    sub = fig.add_subplot(111)
    sub.imshow(matriceGeometrie, cmap='coolwarm', origin='lower')
    ax = fig.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    sub.tick_params(axis='both', which='major', labelsize=6)
    
    #Contour plot
    cp = sub.contourf(P, alpha=0.5)
    plt.clabel(cp)
    fig.colorbar(cp)
    fig.savefig(nom+"-Champ de Pression.pdf")
    
#Function to show the current lines 
def affCourant2(vx, vy, matriceGeometrie, ht=1, maxit=2000, nom='', methode='RK4'):
    #geometry
    fig = plt.figure()
    fig.suptitle('Lignes de Courant (h={})'.format(ht), fontweight='bold')
    sub = fig.add_subplot(111)
    sub.imshow(matriceGeometrie, cmap='coolwarm', origin='lower')
    ax = fig.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    sub.tick_params(axis='both', which='major', labelsize=6)
    
#current lines -------------------------------------------------
    vxc = integrafonct.nantozero(vx)
    vyc = integrafonct.nantozero(vy)
    
    fvx, fvy = integrafonct.interpolation(vxc, vyc, kind='linear')
    
    #to obtain the coordinates of the entry cells (cases d'entree) and exit cells
    matriceNumerotee = geometrie.numeroter(matriceGeometrie)
    nomCases = geometrie.numCases(matriceGeometrie)
    tcoord = geometrie.tableaucoord(matriceGeometrie, matriceNumerotee, nomCases)
    coords = integrafonct.coord(matriceGeometrie, tcoord, nomCases)
    coordentree, coordsortie = coords
    
    #are the entry and exit cells aligned horizontally or vertically?
    #what are the maximum (or minimum) values for the position?
    orient_entree, orient_sortie = integrafonct.orientation(matriceGeometrie,coords)
    shape = matriceGeometrie.shape
    
    if orient_sortie == 'vertical, right':
        typelim = 'xmax'
        lim = shape[1]-1
    elif orient_sortie == 'vertical, left':
        typelim = 'xmin'
        lim = 0
    elif orient_sortie == 'horizontal, up':
        typelim = 'ymin' #the matrix is inverted with respect to the y axis
        lim = 0
    elif orient_sortie == 'horizontal, down':
        typelim = 'ymax'
        lim = shape[0]-1
     
    #Choose the method of integration
    if methode == 'comparaison':
        func1 = integrafonct.trajectoirelim
        func2 = integrafonct.trajectoireRK4
        
        n= 0
        for i,j in coordentree:
            x1,y1 = func1(j,i, fvx, fvy, lim, typelim, tcoord, ht=ht, maxit=maxit)
            x2,y2 = func2(j,i, fvx, fvy, lim, typelim, tcoord, ht=ht, maxit=maxit)
            if n==0:
                sub.plot(x1,y1,'--',color='red', label='Euler')
                sub.plot(x2,y2,'-',color='blue', label='Runge-Kutta 4')
            else:
                sub.plot(x1,y1,'--',color='red')
                sub.plot(x2,y2,'-',color='blue')
            n+=1
            
        sub.legend(loc='upper left')
    
    else:
        if methode == 'Euler':
            func = integrafonct.trajectoirelim
        if methode == 'RK4':
            func = integrafonct.trajectoireRK4
        
        for i,j in coordentree:
            x,y = func(j,i, fvx, fvy, lim, typelim, tcoord, ht=ht, maxit=maxit)
            sub.plot(x,y,'-',color='blue')
    
    #set a limit for each axis
    sub.set_xlim(left=0, right=shape[1])
    sub.set_ylim(bottom=0, top=shape[0])
    
    fig.savefig(nom+"-Lignes de Courant.pdf")
    
#To get the speed profile in a section of the graphic
def ProfilVitesse(vx, vy, numline, horizontal=True, nom=''):
    if horizontal:
        vxp = vx[numline]
        vyp = vy[numline]
        d = 'x '
        title = "Profil de Vitesses "+"(y={})".format(numline)
    else:
        vxp = vx[:,numline]
        vyp = vy[:,numline]
        d = 'y '
        title = "Profil de Vitesses "+"(x={})".format(numline)
        
    fig = plt.figure()
    fig.suptitle(title, fontweight='bold')
    sub = fig.add_subplot(111)
    sub.plot(vxp, label = 'Vx')
    sub.plot(vyp, label = 'Vy')
    sub.legend(loc='upper left')
    sub.set_xlabel(d)
    sub.set_ylabel('Vitesse')
    sub.tick_params(axis='both', which='major', labelsize=6)
    fig.savefig(nom+"-Profil des Vitesses.pdf")
    
#to plot the pressure on the obstacle
def TracePression(P, numline, lmin, lmax, horizontal=True, nom=''):
    if horizontal:
        Pp = P[numline, lmin:(lmax+1):1]
        d = 'x '
        title = "Trace des Pressions "+"(y={})".format(numline)
    else:
        Pp = P[lmin:(lmax+1):1, numline]
        d = 'y '
        title = "Trace des Pressions "+"(x={})".format(numline)
        
    fig = plt.figure()
    fig.suptitle(title, fontweight='bold')
    sub = fig.add_subplot(111)
    sub.plot(Pp)
    sub.set_xlabel(d)
    sub.set_ylabel('Pression')
    sub.tick_params(axis='both', which='major', labelsize=6)
    fig.savefig(nom+"-Trace des Pressions.pdf")

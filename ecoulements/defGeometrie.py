import numpy as np

#here pointsx is the length of the canal, and pointsy its height (minus the two lines in the border if there is one) [unit: pixels] 
def canalh(pointsx, pointsy, border=True): 
    canalh = np.ones((pointsy,pointsx))
    canalh[:,0] = 2*np.ones(pointsy)
    canalh[:,pointsx-1] = 3*np.ones(pointsy)
    
    #walls in the border of the canal (optional)
    if border:
        canalh[0] = np.zeros(pointsx)
        canalh[pointsy-1]= np.zeros(pointsx)
    
    canalh = canalh.astype(int)
    return canalh

#coudex and coudey is the length and height, respectively, of the wall
def canalCoude(pointsx, pointsy, coudex, coudey):
    canalc = np.ones((pointsy, pointsx))
    canalc[:,0] = 2*np.ones(pointsy)
    canalc[0,:] = 3*np.ones(pointsx)
    
    #wall
    for i in range(0, coudey):
        for j in range(0, coudex):
            canalc[i,j] = 0
            
    canalc = canalc.astype(int)
    return canalc

#x0,y0 and xf,yf are the initial and final positions for the obstacle, xy begins at (0,0) and ends at (pointsx-1, pointsy-1)
def canalObstacle(pointsx, pointsy, x0, y0, xf, yf):
    canalo = canalh(pointsx, pointsy, border=False)
    
    #obstacle
    for i in range(y0, yf+1):
        for j in range(x0,xf+1):
            canalo[i,j] = 0
     
    return canalo
    
#l0, lf are the initial and final height of the canal, l0 and lf have to be less than pointsy
def canalElargi(pointsx, pointsy, l0, lf):
    canale = np.zeros((pointsy, pointsx))
    
    #first column (entry)
    esp0 = (pointsy-l0)/2
    for i in range(round(esp0),round(esp0)+l0):
        canale[i, 0] = 2
        
    #last column (exit)
    espf = (pointsy-lf)/2
    for i in range(round(espf),round(espf)+lf):
        canale[i,pointsx-1] = 3
        
    #columns in between
    d_esp = (espf-esp0)/(pointsx-1) 
    
    for j in range(1, pointsx-1):
        esp = d_esp*j + esp0
        for i in range(round(esp),pointsy-round(esp)):
            canale[i,j] = 1
    
    return canale
    
#canal with an circle as an obstacle
def canalcircle(pointsx, pointsy, x0, y0, r):
    canalc = np.ones((pointsy, pointsx))
    canalc[:,0]=2
    canalc[:,pointsx-1]=3
    
    for i in range(0, pointsy):
        for j in range(0, pointsx):
            if np.sqrt((i-y0)**2+(j-x0)**2)<r:
                canalc[i,j]=0
    
    return canalc

#canal with a triangle as an obstacle (triangle with soft corners)
def canaltriang(pointsx, pointsy, x0, y0, a):
    canalc = np.ones((pointsy, pointsx))
    canalc[:,0]=2
    canalc[:,pointsx-1]=3
    
    canalc[x0,y0]= 0
    for i in range(0,pointsy):
        for j in range(0, pointsx):
            y = i - y0
            x = j - x0
            
            cond = (x**2+y**2)**2 + 2*a*x*(x**2-10.5*y**2)+18*a**2*(x**2+y**2)-27*a**4
            cond = int(cond)
            if cond<0:
                canalc[i,j]=0
    
    return canalc
    
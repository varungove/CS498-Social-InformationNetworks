from igraph import *
import random
import numpy as np
import matplotlib.pyplot as plt




def randomTriad():
    a = 10
    b = 10
    c = 10
    while (a==b or b==c or a==c):
        a = np.random.choice(np.arange(0, 10))
        b = np.random.choice(np.arange(0, 10))
        c = np.random.choice(np.arange(0, 10))  
    return a, b, c
        
        
        

    
    
def countBalanced(g):
    ctr=0
    for i in range(0,10):
        for j in range(i+1,10):
            for k in range(j+1,10):
                edgeOne = g.es[g.get_eid(i, j)]["label"]
                edgeTwo = g.es[g.get_eid(i, k)]["label"]
                edgeThree = g.es[g.get_eid(j, k)]["label"]
    
                x = edgeOne + edgeTwo + edgeThree
                if (x==1 or x==3):
                    ctr=ctr+1
    return ctr

def dynamicProcess(g, count):
    a, b, c = randomTriad()
    edgeOne = g.es[g.get_eid(a, b)]["label"]
    edgeTwo = g.es[g.get_eid(b, c)]["label"]
    edgeThree = g.es[g.get_eid(a, c)]["label"]
    
    x = edgeOne + edgeTwo + edgeThree
    
    
    if (x==0 or x==2):
        x = np.random.random_integers(0,2)
        if x==0:
            count = count - optimize(a, b, g)
            if edgeOne==0:
                g.es[g.get_eid(a, b)]["label"]=1
            else:
                g.es[g.get_eid(a, b)]["label"]=0
            count = count + optimize(a, b, g)
        if x==1:
            count = count - optimize(b, c, g)
            if edgeTwo==0:
                g.es[g.get_eid(b, c)]["label"]=1
            else:
                g.es[g.get_eid(b, c)]["label"]=0
            count = count + optimize(b, c, g)
        if x==2:
            count = count - optimize(a, c, g)
            if edgeThree==0:
                g.es[g.get_eid(a, c)]["label"]=1
            else:
                g.es[g.get_eid(a, c)]["label"]=0
            count = count + optimize(a, c, g)
    return g, count
    
    



def initSigns(g):        
    for i in range(0,45):
        g.es[i]["label"] = np.random.choice(np.arange(0, 2), p=[0.5, 0.5])
    return g

def optimize(e, r, g):
    count = 0
    for i in range(0,10):
        if (i!=e and i!=r):
            edgeOne = g.es[g.get_eid(e, r)]["label"]
            edgeTwo = g.es[g.get_eid(e, i)]["label"]
            edgeThree = g.es[g.get_eid(r, i)]["label"]
            x = edgeOne + edgeTwo + edgeThree
            if(x==1 or x==3):
                count=count+1
    return count
        
g = Graph()
n = [0.0] * 1000000
g.add_vertices(10)
g.add_edges([(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9)])
g.add_edges([(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9)])
g.add_edges([(2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9)])
g.add_edges([(3,4), (3,5), (3,6), (3,7), (3,8), (3,9)])
g.add_edges([(4,5), (4,6), (4,7), (4,8), (4,9)])
g.add_edges([(5,6), (5,7), (5,8), (5,9)])
g.add_edges([(6,7), (6,8), (6,9)])
g.add_edges([(7,8), (7,9)])
g.add_edges([(8,9)])



    
       
for j in range(0,100):
    check=0
    g = initSigns(g)
    check = countBalanced(g)
    for i in range(0, 1000000):
        if check!=120:
            g, check = dynamicProcess(g, check)
            
        n[i] = (n[i]+(check/120.0))
        if j==99:
            n[i]=n[i]/100.0
    

x=np.arange(1000000)
plt.figure()
plt.semilogx(x, n, basex=10)
plt.grid(True)
plt.show()


    




    
"""
MP2
@author goverdh2
"""

import csv
import matplotlib.pyplot as plt
from Queue import *
from igraph import *

def parse_graph(g):
    """
    Parses Graph from Data
    :param g: Graph of 200 nodes
    :return g: Rarsed graph g from data
    """
    for i in range(0, 100):
        g.vs[i]['value'] = 0
    with open('preference.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            for j, pref in enumerate(row):
                if(j!=0):
                    g.add_edges([((i+100),j-1)])
                    g.es[g.get_eid((i+100), j-1)]['value'] = pref
    return g

def set_start_prices(g):
    """
    Calculates and sets start price for each round
    :param g: Graph
    :return g: Graph with new start prices
    """
    seller_potential = 0
    min = (int)(g.vs[0]['value'])
    for i in range(1, 100):
        if((int)(g.vs[i]['value']) < min):
            min = (int)(g.vs[i]['value'])
    for i in range(0, 100):
        g.vs[i]['value'] = (int)(g.vs[i]['value']) - min
        seller_potential = seller_potential + g.vs[i]['value']
    return g, seller_potential
    
    
def construct_psg(g):
    """
    Constructs the Preferred Seller Graph and calculates buyer potential
    :param g: Graph 
    :return psg1: Preferred Seller Graph
    :return g: Original graph g
    :return buyer_potential
    """
    psg1 = Graph()
    buyer_potential = 0
    psg1.add_vertices(200)
    
    #Vertices with label 0 are Houses. 
    #Vertices with label 1 are Buyers
    for i in range(0, 200):
        if i<100:
            psg1.vs[i]['label'] = 0
            psg1.vs[i]['value'] = g.vs[i]['value']
        else:
            psg1.vs[i]['label'] = 1
    
    #Calculates max payoff and creates only those edges for each vertex.
    for i in range(0, 100):
        id = g.get_eid(i+100, 0)
        max_id = 0
        max = (int)(g.es[id]['value']) - (int)(g.vs[0]['value'])
        for j in range(0 ,100):
            if((((int)(g.es[g.get_eid(i+100,j)]['value'])) - (int)(g.vs[j]['value'] )) > max):
                max_id = j
                max = (int)(g.es[g.get_eid(i+100,j)]['value']) - (int)(g.vs[j]['value'])
        for k in range(0, 100):
            if ((((int)(g.es[g.get_eid(i+100,k)]['value'])) - (int)(g.vs[k]['value'] )) == max):
                psg1.add_edges([(i+100, k)])
                psg1.es[psg1.get_eid(i+100, k)]['value'] = ((int)(g.es[g.get_eid(i+100,k)]['value']))
        buyer_potential = buyer_potential + max
        
    return psg1, g, buyer_potential
    
def check_if_perfect(constricted_set):
    """
    Checks if there is a perfect matching
    :param constricted_set
    :return bool
    """
    if(len(constricted_set)==0):
        return True
    else:
        return False
        
def get_constricted(psg, matching): 
    """
    Calculates the constrictes set using BFS
    :param psg: Prefferred Seller Graph
    :param matching: Maximal Matching
    :return constricted_set
    """
    que = Queue()
    check = []
    constricted_set = []
    for i in range(100, 200):
        vertex = psg.vs[i]
        if(not (matching.is_matched(vertex))):
            que.put(psg.vs[i])
            constricted_set.append(i)
            break

    while(not que.empty()):
        ver = que.get()
        
        
        if((ver.index)>99):
            l = psg.neighbors(ver)
            if (ver.index not in constricted_set):
                constricted_set.append(ver.index)           
            for v in l:
                if(v not in check):
                    
                    que.put(psg.vs[v])                
        else:
            que.put(matching.match_of(ver))
            check.append(ver.index)
           
    return constricted_set
                    
            
def get_neighbors(psg, constricted_set):
    """
    Calculates neighbours for vertices in constricted set
    :param psg: Preferred Seller Graph
    :param constricted_set
    :return neighbors: List of all neighbours
    """
    neighbors = []
    for vertex in constricted_set:
        l = psg.neighbors(psg.vs[vertex])
        for ver in l:
            if(ver not in neighbors):
                neighbors.append(ver)
    return neighbors
            
def increase_price(g, neighbors):
    """
    Increases price of the constricted set's sellers
    :param g: Graph
    :param neighbors: List of nighbors
    :return g: Graph with prices increased
    """
    for house in neighbors:
        g.vs[house]['value'] = (g.vs[house]['value'])+1
    return g

def write_to_csv(psg, matching):
    """
    Writes all data to csv file
    :param psg: Preferred Seller Graph
    :param matching: Maximal Matching
    """
    results = [[]]
    
    for i in range(100, 200):
        buyer = "buyer"+str(i-100)
        vertex = (matching.match_of(psg.vs[i])).index
        house = "house"+str(vertex)
        payoff = ((int)(psg.es[psg.get_eid(i,vertex)]['value'])) - ((int)(psg.vs[vertex]['value']))
        row = [buyer, house, payoff]
        results.append(row)
    resultFile = open("market-clearing.csv",'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(results)
 

"""
Start of Exectuion.
First 100 nodes are houses.
Second Hundred are Buyers. 
"""
g = Graph()
g.add_vertices(200)
g = parse_graph(g)


check = False
matching = 0

#Count number of rounds
ctr = 1

x_axis = []
y_axis = []


# Loop that runs till rounds are done.
while(not check):
    g, seller_potential = set_start_prices(g)
    psg, g, buyer_potential = construct_psg(g)
    potential_energy = seller_potential + buyer_potential
    x_axis.append(ctr)
    ctr = ctr +1
    y_axis.append(potential_energy)
    matching = psg.maximum_bipartite_matching('label', None, None)
    constricted_set =  get_constricted(psg, matching)
    check = check_if_perfect(constricted_set)
    
    #If there is a perfect match, save and end
    if(check):
        write_to_csv(psg, matching)
        plt.figure()
        plt.xlabel('Rounds')
        plt.ylabel('Potential Energy')
        plt.plot(x_axis, y_axis)
        plt.savefig('potential-energy.jpeg')
        break
        
    neighbors = get_neighbors(psg, constricted_set)
    g = increase_price(g, neighbors)



 

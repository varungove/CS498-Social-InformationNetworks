from igraph import *
import timeit
from Queue import *

def parse_graph(graph_name, g, n):
    """
    Parses and Initializes the Graph
    """
    g.add_vertices(n)
    for i in range(0,n):
        g.vs[i]['value'] = 0.0
        g.vs[i]['parent'] = []
        g.vs[i]['flow'] = 1.0
        g.vs[i]['visited'] = "false"
        g.vs[i]['added'] = "false"
    with open(graph_name, "r") as filestream:
        for row in filestream:
            currentline = row.split(", ")
            num_one = int((currentline[0].split("("))[1])
            num_two = int((currentline[1].split(")"))[0])
            g.add_edges([(num_one, num_two)])
            g.es[g.get_eid(num_one, num_two)]['edge_flow'] = 0.0
        return g

def calculate_mod(g):
    """
    Calculates and returns the modularity of the graph
    """
    comp = g.components()
    sub = comp.subgraphs()
    sum = 0.0
    for ids ,s in enumerate(sub):
        v_list=sub[ids].vs()
        adj=s.get_adjacency()
        deg = s.degree()
        for i in v_list:
            for j in v_list:
                    sum = sum + (adj[i.index][j.index] - ((deg[i.index] * deg[j.index])/(2.0 * g.ecount())))              
    final_sum = (sum/(2.0 * g.ecount()))
    return final_sum

def calc_bet(g, n):
    """
    Calculates the exact betweeness
    """
    start = timeit.default_timer()
    size = len(g.es)
    eb_sums = [0.0]*size
    
    for i in range(0,n):
        g.vs[i]['value'] = 1.0
        q_one = Queue()
        q_two = Queue()
        q_one.put(g.vs[i])
        level_track = []
        l = []
        l.append(g.vs[i])
        g.vs[i]['added'] = "true"
        level_track.append(l)
        counter=0;

        while(q_one.empty() == False):
            v = q_one.get()
            v['visited'] = "true"
            li = g.neighbors(v)
            for ver in li:
                if (g.vs[ver]['visited'] == "false") and g.vs[ver] not in level_track[counter]:
                    g.vs[ver]['value'] = g.vs[ver]['value'] + v['value']
                    g.vs[ver]['parent'].append(v)
                    if (g.vs[ver]['added'] == "false"):
                        q_two.put(g.vs[ver])
                        g.vs[ver]['added'] = "true"
            if q_one.empty():
                l = []
                while not q_two.empty():
                    ver = q_two.get()
                    if ver['visited'] == "false":
                        q_one.put(ver)
                        l.append(ver)
                if len(l)>0:
                    level_track.append(l)
                    counter = counter + 1

        x = len(level_track)
        for i in range(0,x):
            for ver in level_track[x-(i+1)]:
                sum_parents = 0
                for pv in ver['parent']:
                    sum_parents += pv['value']
                for pv in ver['parent']:
                    g.es[g.get_eid(ver, pv)]['edge_flow'] = g.es[g.get_eid(ver, pv)]['edge_flow'] + ((pv['value']/sum_parents)*(ver['flow']))
                    pv['flow'] = pv['flow'] + ((pv['value']/sum_parents)*(ver['flow']))
                    ind = pv.index
                    g.vs[ind]['flow'] = pv['flow']


        for l in g.es:
            idx = l.index
            eb_sums[idx] += l['edge_flow']
            l['edge_flow'] = 0.0

        for i in range(0,n):
            g.vs[i]['parent'] = []
            g.vs[i]['visited'] = "false"
            g.vs[i]['added'] = "false"
            g.vs[i]['value'] = 0.0
            g.vs[i]['flow'] = 1.0
            


    end = timeit.default_timer()
    

    for i in range(0,len(eb_sums)):
        eb_sums[i] = (eb_sums[i] * (0.5))

    fmax = max(eb_sums)
    
    l =  [g.es[idx].tuple for idx, eb in enumerate(eb_sums) if eb == fmax]
    g.delete_edges(l)
    
    return g, len(l), (end-start)

def run_algo(g, n, v_num):
    """
    Runs betweeness algorith until n number of communities are discovered 
    """
    sum_er = 0
    time = 0.0
    while (len(g.components()))<n:
        g, er, t = calc_bet(g, v_num)
        sum_er = sum_er + er
        time = time + t
    return calculate_mod(g), sum_er, time

    

def write_table(st, er, mod):
    """
    Writes and saves the table 
    """
    f = open(st, 'w')
    no = "No of Communities        Cumalitive Number of Edges Removed          Modularity\n"
    one = "      1                        " + str(er[0]) +   "                          "+str(mod[0])+"\n"    
    two = "      2                        " + str(er[1]) +   "                          "+str(mod[1])+"\n"   
    three = "      3                        " + str(er[2]) + "                          "+str(mod[2])+"\n"   
    four = "      4                        " + str(er[3]) +  "                          "+str(mod[3])+"\n"   
    five = "      5                        " + str(er[4]) +  "                          "+str(mod[4])+"\n"   
    f.write(no)
    f.write(one)
    f.write(two)
    f.write(three)
    f.write(four)
    f.write(five)
    f.close()
    
    
    

    
"""
Start of function. Takes user input and begins.
"""
print("Welcome to MP3!")
print("a) Load from Default data")
print("b) Load from Sample Graph")
control = raw_input()

if (control == 'b'):
    """
    Loads Data from sample file and runs calculations.
    """
    
    
    graph = Graph()
    graph = parse_graph("sample.txt", graph, 25)
    print("Running....")
    graph_mod = []
    graph_er = []
    
    edges_rem = 0
    for i in range(1,6):
        """
        Runs algo for 1-5 communities. 
        """
        m, er, t = (run_algo(graph, i, 25))
        edges_rem = edges_rem + er
        graph_mod.append(m)
        graph_er.append(edges_rem)
    write_table("output.txt", graph_er, graph_mod)
    

if (control == 'a'):
    """
    Loads and runs data for each type of graph.
    """
    barabasi_graph = Graph()
    erdos_graph = Graph()
    watts_graph = Graph()

    barabasi_graph = parse_graph("Barabasi.txt", barabasi_graph, 1000)
    erdos_graph = parse_graph("ErdosRenyi.txt", erdos_graph, 1000)
    watts_graph = parse_graph("WattsStrogatz.txt", watts_graph, 1000)
    print("Running....")
    barabasi_mod = []
    erdos_mod =[]
    watts_mod = []

    barabasi_er = []
    erdos_er =[]
    watts_er = []

    times = []

    time = 0.0
    edges_rem = 0
    for i in range(1,6):
        """
        Runs algo for 1-5 communities. 
        """
        m, er, t = (run_algo(barabasi_graph, i, 1000))
        edges_rem = edges_rem + er
        time = time + t
        barabasi_mod.append(m)
        barabasi_er.append(edges_rem)
    times.append(time)

    time = 0.0
    edges_rem = 0
    for i in range(1,6):
        """
        Runs algo for 1-5 communities. 
        """
        m, er, t = (run_algo(erdos_graph, i, 1000))
        edges_rem = edges_rem + er
        time = time + t
        erdos_mod.append(m)
        erdos_er.append(edges_rem)
    times.append(time)

    time = 0.0
    edges_rem = 0
    for i in range(1,6):
        """
        Runs algo for 1-5 communities. 
        """
        m, er, t = (run_algo(watts_graph, i, 1000))
        edges_rem = edges_rem + er
        time = time + t
        watts_mod.append(m)
        watts_er.append(edges_rem)
    times.append(time)


   
    write_table("BarabasiExact.txt", barabasi_er, barabasi_mod)
    write_table("ErdosExact.txt", erdos_er, erdos_mod)
    write_table("WattsExact.txt", watts_er, watts_mod)
    
    print "Times Taken: "
    print times
    

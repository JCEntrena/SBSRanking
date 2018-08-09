# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:31:32 2018

@author: A670679
"""

#idea to generate artificial nodes:
#given a player of a certain tier, at the end of every iteration
#you recalculate it's score based on the score of a similar node 
#f.e: Recalculate a tier2 foreign player doing the avg of nodes 3,4,5


class Win:
    def __init__(self,idL,mult):
        self.idL = idL
        self.mult = mult
class Node:
    def __init__(self,i):
        self.i = i
        self.win = []
        self.lse = []
        self.p = 100
    
class Sim_Node:
    def __init__(self,i,sim):
        self.i = i
        self.nlse = 0
        self.sim = sim
        self.p = 100

graph = []
sim_graph = []
graph_order_act = []
graph_order_old = []
len_graph = 22 #Numero de players registrados en la DB que no son extranjeros

def init_graph():
    global graph
    for i in range(0,len_graph):
        graph.append(Node(i))

def gen_foreign_nodes():
    global sim_graph
    #150 ixis 1 1 1
    sim_graph.append(Sim_Node(0,[1]))
    #151 ho 2-5 2-3 1
    sim_graph.append(Sim_Node(1,[1,2]))
    #152 istu 2-5 5-7 1 
    sim_graph.append(Sim_Node(2,[2,3]))
    #153 meru 6-10 4-6 3-5
    sim_graph.append(Sim_Node(3,[3,4,5,6]))
    #154 light 6-10 5-7 6-7
    sim_graph.append(Sim_Node(4,[5,6,7]))
    #155 longow 3-7 3-5
    sim_graph.append(Sim_Node(5,[2,3,4,5]))
    #156 whyzz 15-20 20-25
    sim_graph.append(Sim_Node(6,[18,19,20,21]))
    #157 storm 20-30 40-45 40-45
    sim_graph.append(Sim_Node(7,[34,35,36,37]))
    #158 tsurugui 20-30 15-20 25-30
    sim_graph.append(Sim_Node(8,[21,22,23,24]))
    #159 dinamirer 9-12 7-10 8-10
    sim_graph.append(Sim_Node(9,[7,8,9,10]))
    #160 gdanzee 40-50 7-10 8-10
    sim_graph.append(Sim_Node(10,[18,19,20,21]))
    #161 simmax 8-10 4-6 8-10
    sim_graph.append(Sim_Node(11,[6,7,8]))
    #162 gregs 15-20 30-35
    sim_graph.append(Sim_Node(12,[23,24,25,26]))
    #163 doublec 20-25 50-55
    sim_graph.append(Sim_Node(13,[35,36,37,38]))
    #164 mrbubu 55-60
    sim_graph.append(Sim_Node(14,[55,56,57,58]))

def act_foreign_nodes():
    global sim_graph
    global graph
    local_graph = list(sorted(graph,key=lambda x: x.p,reverse=True))
    for node in sim_graph:
        p = 0
        nlse = 0
        for sim in node.sim:
            p += local_graph[sim].p
            nlse += len(local_graph[sim].lse)
        node.p = p/len(node.sim)
        node.nlse = nlse/len(node.sim)

def read_graph():
    global graph_order_act
    with open ("h2h_dbdata.txt", "r") as myfile:
        data=myfile.readlines()
    for interaccion in data:
        spc = interaccion.index(" ")
        aW = int(interaccion[0:spc])
        rest = interaccion[spc+1:]
        spc = rest.index(" ")
        aL = int(rest[0:spc])
        tier = str(rest[spc+1:len(rest)-1])
        mult = 0
        if tier == "S":
            mult = 1
        elif tier == "A":
            mult = 0.85
        elif tier == "B":
            mult = 0.75
        elif tier == "C":
            mult = 0.6
        win = Win(aL,mult)
        if aW < len(graph) and aL < len(graph):
            graph[aW].win.append(win)
            graph[aL].lse.append(aW)
        elif aW < len(graph):
            graph[aW].win.append(win)
        else:
            graph[aL].lse.append(aW)
    graph_order_act = range(0,150)

def pagerank():
    global graph
    global sim_graph
    global len_graph
    d = 0.85
    for node in graph:
        farmfactor = 1
        win_ant = -1
        pr = 0
        for win in node.win:
            #si es una win dentro del grafo de SBS:
            if win.idL < len_graph:
                if win_ant == win.idL:
                    farmfactor -=0.1
                    if farmfactor < 0.5:
                        farmfactor = 0.5
                else:
                    farmfactor = 1
                pr += graph[win.idL].p/len(graph[win.idL].lse) * farmfactor * win.mult
                win_ant = win.idL
            #si es una win contra un nodo simulado:
            else:
                if win_ant == win.idL:
                    farmfactor -=0.1
                    if farmfactor < 0.5:
                        farmfactor = 0.5
                else:
                    farmfactor = 1
                pr += sim_graph[win.idL-2000].p/sim_graph[win.idL-2000].nlse * farmfactor * win.mult
                win_ant = win.idL
        prc = (1 - d)/len_graph + d
        node.p = pr + prc
        
def printG():
    global graph
    for node in sorted(graph,key=lambda x: x.p):
        print("Node {0}: {1}".format(node.i,node.p))
  
def printS():
    global graph
    file = open("h2h2db.txt","w")
    for node in graph:
        s = str(node.p) + " " + str(node.i) + "\n"
        file.write(s)
    file.close()
    
def normalize():
    global graph
    max_value = sorted(graph,key=lambda x: x.p)[len(graph)-1].p
    for node in graph:
        node.p = node.p/max_value*100
        
          
def converge():
    global graph
    global graph_order_act
    global graph_order_old
    graph_order_old = list(graph_order_act)
    graph_order_act = []
    for node in sorted(graph,key=lambda x: x.p):
        graph_order_act.append(node.i)
    if graph_order_old == graph_order_act:
        return True
    else:
        return False

def Main():
    init_graph()
    read_graph()
    #gen_foreign_nodes()
    iterations = 0
    while (iterations < 20):
        #act_foreign_nodes()
        pagerank()
        iterations += 1
# =============================================================================
#     while (1):
#         act_foreign_nodes()
#         pagerank()
#         iterations += 1
#         if (converge()):
#             break
# =============================================================================
    normalize()
    printS()
    print("Number of iterations done: {0}".format(iterations))
    
Main()
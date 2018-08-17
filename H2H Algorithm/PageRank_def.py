# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:31:32 2018

@author: A670679
"""

#idea to generate artificial nodes:
#given a player of a certain tier, at the end of every iteration
#you recalculate it's score based on the score of a similar node 
#f.e: Recalculate a tier2 foreign player doing the avg of nodes 3,4,5

import mysql.connector
import math

class Win:
    def __init__(self,idL,mult):
        self.idL = idL
        self.mult = mult
class Node:
    def __init__(self,i):
        self.i = i
        self.win = []
        self.lse = []
        self.tot = {}
        self.nwin = {}
        self.p = 100
        self.p2 = 100
    
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
len_graph = 0
cnx = None
farm_total_f = [None,1,0.97,0.94,0.89,0.812,0.76,0.72286,0.695,0.6733,0.656]
def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot',password='292Hikotsu',host='localhost',database='sys')
    
def get_graphsize():
    global len_graph
    global cnx
    cursor = cnx.cursor()
    query = "SELECT LAST_PID FROM usr_ids  WHERE IDENTIFIER = 'ACT'"
    cursor.execute(query)
    for t in cursor:
        len_graph = t[0] + 1
    
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

def append2dic(aW,aL):
    global graph
    if aL in graph[aW].tot:
        graph[aW].tot[aL] += 1
    else:
        graph[aW].tot[aL] = 1
    if aW in graph[aL].tot:
        graph[aL].tot[aW] += 1
    else:
        graph[aL].tot[aW] = 1
    if aL in graph[aW].nwin:
        graph[aW].nwin[aL] += 1
    else:
        graph[aW].nwin[aL] = 1
def append2dic_L(aW,aL):
    global graph
    if aW in graph[aL].tot:
        graph[aL].tot[aW] += 1
    else:
        graph[aL].tot[aW] = 1

def read_graph():
    global graph_order_act
    global len_graph
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
            append2dic(aW,aL)
        elif aW < len(graph):
            graph[aW].win.append(win)
        else:
            graph[aL].lse.append(aW)
    for i in range(0,len_graph):
        graph[i].win = sorted(graph[i].win,key=lambda x: x.idL,reverse=True)
    graph_order_act = range(0,len_graph)

def act_points():
    global graph
    global sim_graph
    global len_graph
    for i in range(0,len_graph):
        graph[i].p2 = graph[i].p
    
def normalize_i():
    global graph
    global len_graph
    suma = 0
    for i in range(0,len_graph):
        suma += graph[i].p
    for i in range(0,len_graph):
        graph[i].p2 *= len_graph*100/suma
        graph[i].p *= len_graph*100/suma
    

def pagerank():
    global graph
    global sim_graph
    global len_graph
    global farm_total_f
    for ki in range(0,len_graph):
        farmfactor = 1
        win_ant = -1
        pr = graph[ki].p2
        for win in graph[ki].win:
            #si es una win dentro del grafo de SBS:
            if win.idL < len_graph:
                pr += graph[win.idL].p2/graph[ki].tot[win.idL] * win.mult * graph[ki].nwin[win.idL] * farm_total_f[graph[ki].nwin[win.idL]]
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
        graph[ki].p = pr
    act_points()
    normalize_i()
   
    
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
    
def act_wl():
    global cnx
    global graph
    global len_graph
    cursor = cnx.cursor()
    for player in graph:
        nwin = len(player.win)
        nlse = len(player.lse)
        pid = player.i
        query = "UPDATE usr_gen SET WINS =" + str(nwin) + " WHERE PLAYER_ID = " + str(pid)
        cursor.execute(query)
        query = "UPDATE usr_gen SET LOSES =" + str(nlse) + " WHERE PLAYER_ID = " + str(pid)
        cursor.execute(query)
    cnx.commit()

def Main():
    db_connex()
    get_graphsize()
    init_graph()
    read_graph()
    #gen_foreign_nodes()
    iterations = 0
    while (iterations < 500):
        #act_foreign_nodes()
        pagerank()
        iterations += 1
# =============================================================================
#     while (1):
#         #act_foreign_nodes()
#         pagerank()
#         iterations += 1
#         if (converge()):
#             break
# =============================================================================
    print("Number of iterations done: {0}".format(iterations))    
    normalize()
    printS()
    act_wl()
    cnx.close()
    
Main()
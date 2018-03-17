# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:31:32 2018

@author: A670679
"""

import sys
sys.stdout = open('log.txt', 'w')

class Node:
    def __init__(self,i):
        self.i = i
        self.win = []
        self.lse = []
        self.p = 100

graph = []
graph_order_act = []
graph_order_old = []

def init_graph():
    global graph
    for i in range(0,150):
        graph.append(Node(i))

def read_graph():
    global graph_order_act
    with open ("SBS_GRAPH.txt", "r") as myfile:
        data=myfile.readlines()
    data[0] = data[0][3:]
    for interaccion in data:
        spc = interaccion.index(" ")
        aL = int(interaccion[0:spc])
        aW = int(interaccion[spc+1:])
        graph[aW].win.append(aL)
        graph[aL].lse.append(aW)
    graph_order_act = range(0,150)

def pagerank():
    global graph
    for node in graph:
        farmfactor = 1
        win_ant = -1
        pr = 0
        for win in node.win:
            if win_ant == win:
                farmfactor -=0.1
                if farmfactor < 0.5:
                    farmfactor = 0.5
            else:
                farmfactor = 1
            pr += graph[win].p/len(graph[win].lse) * farmfactor
            win_ant = win
        node.p = pr

def printG():
    global graph
    for node in sorted(graph,key=lambda x: x.p):
        print("Node {0}: {1}".format(node.i,node.p))
  
def printS():
    global graph
    for node in graph:
        print(node.p)

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
    iterations = 0
    while (iterations < 100):
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
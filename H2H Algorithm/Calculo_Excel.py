# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 13:52:07 2018

@author: A670679
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:31:32 2018

@author: A670679
"""

import sys
sys.stdout = open('log2.txt', 'w')

class Node:
    def __init__(self,i):
        self.i = i
        self.win = []
        self.lse = []
        self.p = 1
        self.p2 = 1

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

def move_p():
    global graph
    for node in graph:
        node.p2 = node.p
     
def las_mates():
    global graph
    for node in graph:
        p = 0
        for win in node.win:
            p += graph[win].p2
        node.p = p
    move_p()

def printG():
    global graph
    for node in graph:
        print("Node {0}: {1}".format(node.i,node.p))
  
def normalize():
    global graph
    graph = sorted(graph,key=lambda x: x.p)
    max_value = graph[len(graph)-1].p
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
    while (1):
        las_mates()
        iterations += 1
        if (converge()):
            break
    normalize()
    printG()
    print("Number of iterations done: {0}".format(iterations))
    
Main()
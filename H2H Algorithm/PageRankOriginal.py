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
        pr = 0
        for win in node.win:
            pr += graph[win].p/len(graph[win].lse)
        node.p = pr

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
        pagerank()
        iterations += 1
        if (converge()):
            break
    normalize()
    printG()
    print("Number of iterations done: {0}".format(iterations))
    
Main()
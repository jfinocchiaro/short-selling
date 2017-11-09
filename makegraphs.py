import numpy as np
import networkx as nx

def starGraph(n):
    #n is the number of edges, 0 is the center, has n-1 nodes
    G = nx.Graph()
    for i in range(1,n):
        G.add_edge(0, i) #add edge from 0 to spoke
        G.add_edge(i,0) #make it undirected
    return G

def ringGraph(n):
    G = nx.Graph()
    for i in range(n):
        G.add_edge(i, (i+1) % n) #add edge to right
        G.add_edge(i, (i-1) % n) #add edge to left

    return G

def clique(n):
    #fully connected graph
    return nx.complete_graph(n)

def lattice(n):
    #n-by-n lattice grid
    return nx.grid_graph(dim=[n,n])

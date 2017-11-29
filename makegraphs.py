import numpy as np
import networkx as nx

def starGraph(n, center):
    #n is the number of edges, 1 is the center, has n-1 nodes on the outside
    G = nx.Graph()
    for i in range(1,n):
        G.add_edge(center, i) #add edge from 1 to spoke
        G.add_edge(i,center) #make it undirected
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

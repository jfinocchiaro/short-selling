import numpy as np
import networkx as nx

def starGraph(n):
    #n is the number of edges, 1 is the center, has n-1 nodes on the outside
    G = nx.Graph()
    for i in range(2,n+1):
        G.add_edge(1, i) #add edge from 1 to spoke
        G.add_edge(i,1) #make it undirected
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

def ec_toy():
    G = nx.Graph()
    G.add_edge(1,2)
    G.add_edge(1,3)
    G.add_edge(1,4)
    G.add_edge(1,5)
    G.add_edge(1,6)
    G.add_edge(2,3)
    G.add_edge(2,6)
    G.add_edge(2,7)
    G.add_edge(3,4)
    G.add_edge(4,5)
    G.add_edge(5,6)

    G.add_edge(2,1)
    G.add_edge(3,1)
    G.add_edge(4,1)
    G.add_edge(5,1)
    G.add_edge(6,1)
    G.add_edge(3,2)
    G.add_edge(6,2)
    G.add_edge(7,2)
    G.add_edge(4,3)
    G.add_edge(5,4)
    G.add_edge(6,5)

    return G

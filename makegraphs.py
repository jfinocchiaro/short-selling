import numpy as np
import networkx as nx
import agents
from agents import Agent

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


agent_type = {0: [[10.0, 1.0],[1.0, 0.0]], 1: [[1.0, 10.0],[0.0, 1.0]], 2: [[10.0, 10.0], [0.01, 0.01]], 3: [[10.0, 1.0], [0.0, 1.0]], 4: [[1.0, 10.0],[0.0, 1.0]]}

def assignAgents(G):
    
    print("Assigning nodes");
 
    agentlist = {};

    agentlist[0] = Agent(0, np.array(agent_type[2][0]), np.array(agent_type[2][1]), np.array([0,0]));
    for node in G.nodes()[1:]:
        config = np.random.randint(5);
        print(node, config);
        agent_configuration = agent_type[config];
        agentlist[node] = (Agent(node, np.array(agent_configuration[0]), 
                               np.array(agent_configuration[1]), 
                               np.array([0,0])));
    
    return agentlist;

       

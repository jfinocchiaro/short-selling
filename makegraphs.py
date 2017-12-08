import numpy as np
import networkx as nx
import agents
from agents import Agent
from networkx.algorithms import bipartite

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

def bipartiteGraph(n):
    return bipartite.random_graph(n,n,0.5);
    

def ERGraph(n,p):
    return nx.erdos_renyi_graph(n,p);

agent_type = {0: [[10.0, 1.0], [0.01, 0.99]], 1: [[1.0, 10.0],[0.99, .01]], 2: [[10.0, 10.0], [0.01, 0.01]], 3: [[10.0, 1.0],[0.99, 0.01]], 4: [[1.0, 10.0],[0.01, .99]]}

def assignAgents(G):
    
    print("Assigning nodes");
 
    agentlist = {};

    agentlist[0] = Agent(0, np.array(agent_type[2][0]), np.array(agent_type[2][1]), np.array([0,0]));
    for node in G.nodes()[1:]:
        config = np.random.randint(3);
        print(node, config);
        agent_configuration = agent_type[config];
        agentlist[node] = (Agent(node, np.array(agent_configuration[0]), 
                               np.array(agent_configuration[1]), 
                               np.array([0,0])));
    
    return agentlist;

def assignAgentsRandom(G, num_goods):
    
    agentlist = {};

    for node in G.nodes():
        agent_util = np.random.random(size=(num_goods,));
        agent_endowment = np.random.random(size=(num_goods,));
        agent_endowment = agent_endowment / np.linalg.norm(agent_endowment);
        agentlist[node] = (Agent(node, np.array(agent_util), 
                               np.array(agent_endowment), 
                               np.array([0,0])));
    
    return agentlist;

def assignAgentsSelectiveRandom(G, num_goods, num_types):
     
    agent_type = {};
    for i in range(num_types):
       agent_type[i] = [10*np.random.random(num_goods), np.random.random(num_goods)];
       print(agent_type[i]);

        
    agentlist = {};
    for node in G.nodes():
        config = np.random.randint(num_types);
        print(node, config);
        agent_configuration = agent_type[config];
        agentlist[node] = (Agent(node, np.array(agent_configuration[0]), 
                               np.array(agent_configuration[1]), 
                               np.array([0,0]), agent_type=config));
    
    return agentlist;

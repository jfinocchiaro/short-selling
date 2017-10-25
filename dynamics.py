import networkx as nx
import numpy as np
import agents
from collections import defaultdict

if __name__ == "__main__":
    G = nx.Graph()

    #initialize graph here

    c = 2 #number of commodities
    agentlist = defaultdict(Agent)
    for i in range(G.number_of_nodes()):
        #initialize params for agent
        # u = np.zeros(c)
        # e = np.ones(c)
        # p = np.ones(c)
        #subplans = np.zeros((G.number_of_nodes(),c))
        agentlist[i] = Agent(u, e, p, subplans)

import networkx as nx
import numpy as np
import agents
from collections import defaultdict
import matplotlib.pyplot as plt
import makegraphs

def checkEquilibrium(G_old, G_new):
    pass


def drawNetwork(G, filename):
    limits = plt.axis('off') #turn off axes
    nx.draw(G, pos=nx.spring_layout(G))
    plt.savefig(filename)




if __name__ == "__main__":
    G = makegraphs.ringGraph(5)
    drawNetwork(G, 'test.png')
    #initialize graph here
    '''
    c = 2 #number of commodities
    agentlist = defaultdict(Agent)
    for i in range(G.number_of_nodes()):
        #initialize params for agent
        # u = np.zeros(c)
        # e = np.ones(c)
        # p = np.ones(c)
        #subplans = np.zeros((G.number_of_nodes(),c))
        agentlist[i] = Agent(u, e, p, subplans)

    '''

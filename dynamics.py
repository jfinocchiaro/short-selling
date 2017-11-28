import networkx as nx
import numpy as np
import agents
from agents import Agent
from collections import defaultdict
import matplotlib.pyplot as plt
import makegraphs
import convex_optimization
from decimal import Decimal
import linear_iterative

#DONE
def checkEquilibrium(agents_old, agents_new):
    #if G_old == G_new: return True

    #check every agent's subplan
    for agent in agents_old:
        for person in range(agents_old[agent].subplans.shape[0]):
            sublabels_old = [float(Decimal('%.2f' % elem)) for elem in list(agents_old[agent].subplans.T[0])]
            sublabels_new = [float(Decimal('%.2f' % elem)) for elem in list(agents_new[agent].subplans.T[0])]
            print sublabels_old == sublabels_new
            if (sublabels_old == sublabels_new):
                pass
            else:
                return False

    return True

#TODO: Check approximate equilibrium if we never hit actual


#Add node subplans to drawing
def drawNetwork(G, attribute, filename):
    limits = plt.axis('off') #turn off axes
    attr = nx.get_node_attributes(G, attribute)
    labels = {}

    for agent in attr.itervalues():
        sublabels = [float(Decimal('%.2f' % elem)) for elem in list(agent.e)]
        labels[agent.idnum] = [agent.idnum, agent.calcUtility(), sublabels]
    nx.draw(G, pos=nx.spring_layout(G), labels=labels)
    plt.savefig(filename)


def changePlans(G):
    #get dict of agents
    agentlist = nx.get_node_attributes(G, 'agentprop')

    #buying sweep
    #do as vector operations?
    #max utility subject to budget constraints
    for node in G.nodes():
        agentlist[node] = linear_iterative.optimizelinearutility(agentlist[node], G, agentlist)


    return agentlist
    #return dictionary of agents



if __name__ == "__main__":
    G = makegraphs.ringGraph(3)
    #initialize graph here

    c = 2 #number of commodities
    agentlist = defaultdict(Agent)
    for i in range(G.number_of_nodes()):
        #initialize params for agent
        u = np.zeros(c)
        e = np.ones(c)
        p = np.ones(c)
        subplans = np.zeros((G.number_of_nodes(),c))
        agentlist[i] = Agent(u, e, p, subplans)

    nx.set_node_attributes(G, 'agentprop', agentlist)

    check_eq = False
    num_rounds = 0
    while (check_eq):
        agents_old = nx.get_node_attributes(G, 'agentprop')
        agents_new = changePlans(G)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        check_eq = checkEquilibrium(agents_old, agents_new)
        num_rounds += 1

    print (str(num_rounds - 1) + ' rounds needed to reach equilibrium.')


    drawNetwork(G, 'agentprop', 'test.png')

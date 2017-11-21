import networkx as nx
import numpy as np
import agents
from collections import defaultdict
import matplotlib.pyplot as plt
import makegraphs
import convex_optimization


#DONE
def checkEquilibrium(agents_old, agents_new):
    #if G_old == G_new: return True

    #check every agent's subplan
    for agent in agents_old:
        for person in range(agents_old[agent].subplans.shape[0]):
            print (agents_old[agent].subplans[person])
            print (agents_new[agent].subplans[person])
            print (agents_old[agent].subplans[person] == agents_old[agent].subplans[person])
            if (agents_old[agent].subplans[person] == agents_new[agent].subplans[person]).all():
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
        print (agent)
        labels[agent.idnum] = [agent.idnum, agent.calcUtility(), agent.subplans]
    nx.draw(G, pos=nx.spring_layout(G), labels=labels)
    plt.savefig(filename)


def changePlans(G):
    #get dict of agents
    agentlist = nx.get_node_attributes(G, 'agentprop')

    #buying sweep
    #do as vector operations?
    #max utility subject to budget constraints
    for node in G.nodes():
        agentlist[node] = convex_optimization.optimizelinearutility(agentlist[node], G, agentlist)

    return agentlist
    #return dictionary of agents



if __name__ == "__main__":
    G = makegraphs.ringGraph(5)
    drawNetwork(G, 'test.png')
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

import networkx as nx
import numpy as np
import agents
from collections import defaultdict
import matplotlib.pyplot as plt
import makegraphs


#DONE
def checkEquilibrium(agents_old, agents_new):
    #if G_old == G_new: return True

    #check every agent's subplan
    for agent in agents_old:
        if list(agents_old[agent].subplans) == list(agents_new[agent].subplans):
            pass
        else:
            return False

    return True

#TODO: Check approximate equilibrium if we never hit actual


#Add node subplans to drawing
def drawNetwork(G, attribute, filename):
    limits = plt.axis('off') #turn off axes
    nx.draw(G, pos=nx.spring_layout(G))
    plt.savefig(filename)


def changePlans(G):
    #get dict of agents
    agentlist = G.get_node_attributes(G, 'agentprop')

    #buying sweep
    #do as vector operations?
    #max utility subject to budget constraints
    for node in G.nodes():
        agent = agentlist[node]

        for neighbor in G.neighbors(node):
            items_to_sell = agentlist[neighbor].endowment_plan
            prices = agentlist[neighbor].p
            for item in range(len(items_to_sell)):
                #optimize plan

    #re-selling sweep
    for node in G.nodes():
        pass

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
    while (!check_eq):
        agents_old = nx.get_node_attributes(G, 'agentprop')
        agents_new = changePlans(G)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        check_eq = checkEquilibrium(agents_old, agents_new)
        num_rounds += 1

    print str(num_rounds - 1) + ' rounds needed to reach equilibrium.'

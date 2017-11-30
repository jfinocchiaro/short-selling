import agents
from agents import Agent
import convex_optimization
import makegraphs
import dynamics
import networkx as nx
import numpy as np
import copy
from collections import defaultdict

def main():
    G = makegraphs.starGraph(1000,0)
    #G = makegraphs.clique(5);
    #G = makegraphs.ringGraph(1000)
    agentlist = makegraphs.assignAgents(G);
    #id num, utility, endowment, prices

    num_goods = 2

    nx.set_node_attributes(G, 'agentprop', agentlist)

    check_eq = False
    num_rounds = 0

    while (check_eq == False):
        print("Num rounds:  %i" % num_rounds);
        agents_old = copy.deepcopy(nx.get_node_attributes(G, 'agentprop'));
        agents_new = dynamics.changePlans(G)
        check_eq = dynamics.checkEquilibrium(agents_old, agents_new)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        filename = 'samplefile' + str(num_rounds) + '.png'
        #dynamics.drawNetwork(G, 'agentprop', filename)
        num_rounds += 1

    print('Number of rounds to reach equilibrium:\t%i' % num_rounds)

    nx.set_node_attributes(G, 'agentprop', agentlist)

    dynamics.drawNetwork(G, 'agentprop', 'samplefile.png')




if __name__ == '__main__':
    main()

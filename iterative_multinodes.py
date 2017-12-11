import agents
from agents import Agent
import convex_optimization
import makegraphs
import dynamics
import networkx as nx
import numpy as np
import copy
from collections import defaultdict
import analyze

def main():
    #G = makegraphs.starGraph(1000,0)
    #G = makegraphs.clique(5);
    #G = makegraphs.ringGraph(1000)

    num_goods = 2
    num_types = 4 # This is the type of agents you want to assign
    #G = makegraphs.ERGraph(100,0.1)
    #G = makegraphs.bipartiteGraph(200);
    G = makegraphs.ConfigurationModel(1000);
    agentlist = makegraphs.assignAgentsSelectiveRandom(G, num_goods, num_types);
    nx.set_node_attributes(G, 'agentprop', agentlist)
    #G = makegraphs.ReadModel('./graphfile');
    #agentlist = nx.get_node_attributes(G, 'agentprop');

    for node in G.nodes():
        agent = agentlist[node];
	agent.u_init = agent.calcUtility();

    check_eq = False
    num_rounds = 0
    pos = nx.spring_layout(G);

    while (check_eq == False):
        print("Num rounds:  %i" % num_rounds);
        filename = 'barter' + str(num_rounds) + '.png'
        #dynamics.drawNetwork(G, pos, 'agentprop', filename)
        agents_old = copy.deepcopy(nx.get_node_attributes(G, 'agentprop'));
        agents_new = dynamics.changePlans(G)
        check_eq = dynamics.checkEquilibrium(agents_old, agents_new)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        #dynamics.drawNetwork(G, 'agentprop', filename)
        num_rounds += 1

    print('Number of rounds to reach equilibrium:\t%i' % num_rounds)

    nx.set_node_attributes(G, 'agentprop', agentlist)
    
    filename = 'barter' + str(num_rounds) + '.png'

    analyze.process_centrulity(G, num_types);

    nx.write_yaml(G, 'graphfile')
    #dynamics.drawNetwork(G, pos, 'agentprop', filename)


if __name__ == '__main__':
    main()

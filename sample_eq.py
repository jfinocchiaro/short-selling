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
    G = makegraphs.starGraph(3)
    agentlist = {}
    #id num, utility, endowment, prices
    agent2 = Agent(2, np.array((10,1)), np.array((0,1)), np.array((1, 1)))
    agentlist[2] = agent2

    agent1 = Agent(1, np.array((10,10)), np.array((0,0)), np.array((10,10)))
    agentlist[1] = agent1

    agent3 = Agent(3, np.array((1,10)), np.array((1,0)), np.array((1,1)))
    agentlist[3] = agent3


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

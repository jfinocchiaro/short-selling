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
    agent2 = Agent(2, np.array((10.0,1.0)), np.array((0.1,0.8)), np.array((1.0, 1.0)))
    agentlist[2] = agent2

    agent1 = Agent(1, np.array((10.0,10.0)), np.array((0.1,0.1)), np.array((10.0,10.0)))
    agentlist[1] = agent1

    agent3 = Agent(3, np.array((1.0,10.0)), np.array((0.8,0.1)), np.array((1.0,1.0)))
    agentlist[3] = agent3


    num_goods = 2

    nx.set_node_attributes(G, 'agentprop', agentlist)

    check_eq = False
    num_rounds = 0

    pos = nx.spring_layout(G);

    while (check_eq == False):
        print("Num rounds:  %i" % num_rounds);
        filename = 'barter' + str(num_rounds) + '.png'
        dynamics.drawNetwork(G, pos, 'agentprop', filename)
        agents_old = copy.deepcopy(nx.get_node_attributes(G, 'agentprop'));
        agents_new = dynamics.changePlans(G)
        check_eq = dynamics.checkEquilibrium(agents_old, agents_new)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        num_rounds += 1

    print('Number of rounds to reach equilibrium:\t%i' % num_rounds)

    nx.set_node_attributes(G, 'agentprop', agentlist)

    filename = 'barter' + str(num_rounds) + '.png'
    dynamics.drawNetwork(G, pos, 'agentprop', filename)




if __name__ == '__main__':
    main()

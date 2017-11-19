import agents
from agents import Agent
import convex_optimization
import makegraphs
import dynamics
import networkx as nx
import numpy as np
from collections import defaultdict

def main():
    G = makegraphs.starGraph(5)
    agentlist = {}
    #id num, utility, endowment, prices, subplans, r
    agent1 = Agent(1, np.array((10,1)), np.array((0,1)), np.array((10, 10)), np.array([[0,0], [3,0]]), np.array([0,1]))
    agentlist[1] = agent1

    agent2 = Agent(2, np.array((10,10)), np.array((0,0)), np.array((10,10)), np.array([[0, 3], [0,0]]), np.array([1, 1]))
    agentlist[2] = agent2

    agent3 = Agent(3, np.array((1,10)), np.array((1,0)), np.array((10,10)), np.array([[0,0], [3,0]]), np.array([1, 0]))
    agentlist[3] = agent3

    agent4 = Agent(4, np.array((10,10)), np.array((0,0)), np.array((10,10)), np.array([[0, 3], [0,0]]), np.array([1, 1]))
    agentlist[4] = agent4

    agent5 = Agent(5, np.array((1,10)), np.array((1,0)), np.array((10,10)), np.array([[0,0], [3,0]]), np.array([1, 0]))
    agentlist[5] = agent5


    nx.set_node_attributes(G, 'agentprop', agentlist)

    check_eq = False
    num_rounds = 0

    while (check_eq == False):
        agents_old = nx.get_node_attributes(G, 'agentprop')
        agents_new = dynamics.changePlans(G)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        check_eq = dynamics.checkEquilibrium(agents_old, agents_new)
        filename = 'samplefile' + str(num_rounds) + '.png'
        dynamics.drawNetwork(G, 'agentprop', filename)

        num_rounds += 1

    print(num_rounds-1)

    nx.set_node_attributes(G, 'agentprop', agentlist)

    #dynamics.drawNetwork(G, 'agentprop', 'samplefile.png')




if __name__ == '__main__':
    main()

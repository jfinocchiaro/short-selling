#from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict
import dynamics

def buyGoods(ag, G, agentlist):
    #agent is idnumber of agent

    #endowmentplan is a buying plan

    agent = agentlist[ag]
    most_desired = [i[0] for i in sorted(enumerate(agent.u), reverse=True, key=lambda x:x[1])]
    print (most_desired)
    spending_money = np.dot(agent.endowmentplan, agent.p) + agent.money
    print 'Spending money:\t' + str(spending_money)
    for nei in G.neighbors(ag):
        neighbor = agentlist[nei]
        #COMMENCE THE TRADE
        for item in most_desired:
            while neighbor.endowmentplan[item] > 0 and spending_money > 0.01 * neighbor.p[item]:
                #if neighbor.endowmentplan[item] * neighbor.p[item] <= spending_money:
                #print('Spending money: %d' % spending_money)
                neighbor.endowmentplan[item] -= 0.01
                neighbor.money += 0.01 * neighbor.p[item]

                agent.endowmentplan[item] +=  0.01

                agent.money -= 0.01 * neighbor.p[item]

    print 'Agent endowment: \t' + str(agent.e) + '\tendowment plan:\t' + str(agent.endowmentplan)

        #AKA I'm super lost

    return agent

def changePlans(G,agentlist):
    for agent in G.nodes():
        agentlist[agent] = buyGoods(agent, G, agentlist)

    for agent in G.nodes():
        #check_clear is set to the amount of items it plans to have after selling
        agentlist[agent].check_clear = agentlist[agent].endowmentplan - agentlist[agent].e

        print ('Check clear' + str(agentlist[agent].check_clear))
    return agentlist

def checkClear(G, agentlist):
    for agent in G.nodes():
        if (agentlist[agent].check_clear != np.zeros((c,1))).all():
            return False

    return True


def adjustPrices(agentlist, check_clear):
    for agent in agentlist.itervalues():
        for i in range(agent.check_clear.shape[0]):
            if np.around(agent.check_clear[i], 2)  > 0:
                #prices too high
                agent.p[i] -= (agent.check_clear[i])
            elif np.around(agent.check_clear[i], 2) < 0:
                #prices too low
                agent.p[i] += (agent.check_clear[i])
        agentlist[agent.idnum] = agent
    return agentlist

def startEconomy(G,agentlist):
    check_clear = False
    num_rounds = 0
    while (check_clear == False):
        #agents_old = copy.deepcopy(nx.get_node_attributes(G, 'agentprop'));
        #agentlist = nx.get_node_attributes(G, 'agentprop')
        agentlist = adjustPrices(agentlist, check_clear)
        agents_new = changePlans(G, agentlist)
        check_clear = checkClear(G, agents_new)
        nx.set_node_attributes(G, 'agentprop', agents_new)
        num_rounds += 1

    print('Rounds played:  '+ str(num_rounds))

    return G


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1,2)
    G.add_edge(2,3)
    c = 2
    agentlist = defaultdict(Agent)
    #id num, utility, endowment, prices, subplans,
    agent1 = Agent(1, np.array((10,1)), np.array((0.01,0.98)), np.array((10, 10)))
    agentlist[1] = agent1

    agent2 = Agent(2, np.array((10,10)), np.array((0.01,0.01)), np.array((10,10)))
    agentlist[2] = agent2

    agent3 = Agent(3, np.array((1,10)), np.array((0.98,0.01)), np.array((10,10)))
    agentlist[3] = agent3


    nx.set_node_attributes(G, 'agentprop', agentlist)
    G = startEconomy(G, agentlist)
    dynamics.drawNetwork(G, 'agentprop', 'samplefrench.png')

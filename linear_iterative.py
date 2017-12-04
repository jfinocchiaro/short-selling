#from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict
import copy

def calcTrade(agent, neighbor):
    num_goods = len(agent.e)
    bought_items = np.zeros(num_goods)
    sold_items = np.zeros(num_goods)
    #neighbor = agentlist[nei]
    agent_e = copy.deepcopy(agent.e);
    neighbor_e = copy.deepcopy(neighbor.e); 
    
    for item_num1, copies1 in enumerate(agent.e):
        for item_num2, copies2 in enumerate(neighbor.e):
            #neighbor gives agent item 1, agent gives neighbor item 2
            if neighbor.u[item_num1] < agent.u[item_num1] and neighbor.u[item_num2] >= agent.u[item_num2]:
                print 'engaged in trade'
                print agent.e
                print neighbor.e
                num_traded = min(neighbor_e[item_num1], agent_e[item_num2])
                bought_items[item_num1] += num_traded
                sold_items[item_num2] += num_traded

                agent_e[item_num1] += num_traded;
                neighbor_e[item_num2] += num_traded;
                
                agent_e[item_num2] -= num_traded;
                neighbor_e[item_num1] -= num_traded;
                #bought_items[item_num1] += neighbor.e[item_num1]
                #sold_items[item_num2] += agent.e[item_num2]


    return bought_items.T, sold_items.T

def optimizelinearutility(agent, G, agentlist):

    num_goods = len(agent.e)

    for nei in G.neighbors(agent.idnum):
        neighbor = agentlist[nei]
        neighbor_util = neighbor.u

        #bought_items = np.zeros((num_goods,1))
        #sold_items = np.zeros((num_goods,1))

        #perform trade

        bought_items, sold_items = calcTrade(agent, neighbor)

        print bought_items
        print sold_items
        print 'Neighbor ' + str(neighbor.idnum) + ' endowment ' + str(neighbor.e)

        neighbor.e += sold_items
        neighbor.e -= bought_items
        agent.e += bought_items
        agent.e -= sold_items

    return agent

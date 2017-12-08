import networkx as nx
import numpy as np
from collections import defaultdict

class Agent:
    def __init__(self, idnum, utility, endowment,  prices, loan=0.0):
        self.idnum = idnum
        self.u = utility.T #vector dim c x 1 of coefficients for each commodity c
        self.e = endowment.T #vector dim c x 1
        self.endowmentplan = endowment.T
        self.p = prices.T #vector dim c x 1
        c = len(self.u)
        self.x = defaultdict(list)  #dict of what an agent plans to buy from each neighbor (indexed by neighbor)

        self.r = np.zeros((c,1))
        self.k = np.zeros((c,1))
        self.budget_constraint_ineq = np.matmul(self.p, (self.e + self.r))
        #self.check_clear = np.zeros((c,1))
        self.money = loan
        self.demand = []
        #self.budget_constraint_eq = (r + k).T

    def calcUtility(self):
        itemutil = (np.dot(self.u, self.e))
        moneyutil = self.money
        return (itemutil + moneyutil)

    def budgetconstraint(self, G):
        budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            agent_neighbor = G.node[neighbor]['agentprop']
            plan_fromneighbor = np.matmul(agent_neighbor.p.T, self.subplans)

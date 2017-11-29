import networkx as nx
import numpy as np


class Agent:
    def __init__(self, idnum, utility, endowment,  prices):
        self.idnum = idnum
        self.u = utility.T #vector dim c x 1 of coefficients for each commodity c
        self.e = endowment.T #vector dim c x 1
        self.endowmentplan = endowment.T
        self.p = prices.T #vector dim c x 1
        c = len(self.u)
        self.subplans = np.zeros((c,1)) #vector dimension (num_agents) x c
        self.x = np.sum(self.subplans)
        self.r = np.zeros((c,1))
        self.k = np.zeros((c,1))
        self.budget_constraint_ineq = np.matmul(self.p, (self.e + self.r))
        self.check_clear = np.zeros((c,1))
        self.money = 0
        #self.budget_constraint_eq = (r + k).T

    def calcUtility(self):
        return (np.dot(self.u, self.subplans))

    def budgetconstraint(self, G):
        budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            agent_neighbor = G.node[neighbor]['agentprop']
            plan_fromneighbor = np.matmul(agent_neighbor.p.T, self.subplans)

import networkx as nx
import numpy as np


class Agent:
    def __init__(self, idnum, utility, endowment,  prices, subplans, r, k):
        self.idnum = idnum
        self.u = utility #function
        self.e = endowment.T #vector dim c x 1
        self.endowment_plan = endowment.T #how much the person would have after they sell if they sold right now
        self.p = prices.T #vector dim c x 1
        self.subplans = subplans #vector dimension (num_agents) x c
        self.x = np.sum(subplans)
        self.r = r.T #vector dim c x 1, commodity to resell
        self.k = k.T #vector dim c x 1, commodity to keep
        self.budget_constraint_ineq = np.matmul(self.p, (self.endowment_plan + r))
        self.budget_constraint_eq = (r + k).T

    def budgetconstraint(self, G):
        budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            agent_neighbor = G.node[neighbor]['agentprop']
            plan_fromneighbor = np.matmul(agent_neighbor.p.T, self.subplans)

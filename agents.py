import networkx as nx
import numpy as np


class Agent:
    def __init__(self, idnum, utility, endowment,  prices, subplans, lambdafunc):
        self.idnum = idnum
        self.u = utility.T #vector dim c x 1 of coefficients for each commodity c
        self.e = endowment.T #vector dim c x 1
        #removed endowment plan since it is calculated e + r
        #self.endowment_plan = endowment.T #how much the person would have after they sell if they sold right now
        self.p = prices.T #vector dim c x 1
        self.subplans = subplans #vector dimension (num_agents) x c
        self.x = np.sum(subplans)
        self.lambdafunc = lambdafunc #cx1 vector of proportion of a good to resell
        c = len(self.u)
        self.r = np.zeros((c,1))
        self.k = np.zeros((c,1))
        self.budget_constraint_ineq = np.matmul(self.p, (self.e + self.r))
        #self.budget_constraint_eq = (r + k).T

    def budgetconstraint(self, G):
        budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            agent_neighbor = G.node[neighbor]['agentprop']
            plan_fromneighbor = np.matmul(agent_neighbor.p.T, self.subplans)

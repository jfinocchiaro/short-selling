import networkx as nx
import numpy as np


class Agent:
    def __init__(self, id, utility, endowment, endowment_plan, prices, subplans):
        self.id = id
        self.u = utility #function
        self.e = endowment #vector dim c x 1
        self.endowment_plan = endowment_plan #how much the person would have after they sell if they sold right now
        self.p = prices #vector dim c x 1
        self.subplans = subplans #vector dimension (num_agents) x 1
        self.x = np.sum(subplans)

        #self.budget_constraint = sum(np.multiply(p, e))

    def budgetconstraint(self, G):
        self.budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            self.budget_constraint += subplans[neighbor]

import networkx as nx
import numpy as np
import copy


class Agent:
    def __init__(self, idnum, utility, endowment,  prices):
        self.idnum = idnum
        self.u = utility.T #vector dim c x 1 of coefficients for each commodity c
        c = len(self.u)
        self.e = endowment.T #vector dim c x 1
        self.e_init = copy.deepcopy(endowment.T)
        self.p = prices.T #vector dim c x 1
        self.subplans = np.zeros((c,1)) #vector dimension c x 1 of what to buy from each neighbor
        self.x = []
        #self.lambdafunc = lambdafunc #cx1 vector of proportion of a good to resell
        #self.r = np.zeros((c,1))
        #self.k = np.zeros((c,1))
        self.sellplan = np.zeros((c,1))
        self.resell = np.zeros((c,1))
        #self.budget_constraint_ineq = np.matmul(self.p, (self.e + self.r))
        #self.budget_constraint_eq = (r + k).T

    def calcUtility(self):
        '''
        print 'Agent num %i' % self.idnum
        print 'Agent utility ' + str(self.u)
        print 'Agent endowment ' + str(self.e)
        print 'Agent subplans ' + str(self.subplans)
        print 'Agent sellplan ' + str(self.sellplan)
        print 'Agent resell ' + str(self.resell)
        '''
        return np.dot(self.u, self.e)

        #return (np.dot(self.u, (self.e + self.subplans)))

    def budgetconstraint(self, G):
        budget_constraint = 0

        for neighbor in G.neighbors(self.id):
            agent_neighbor = G.node[neighbor]['agentprop']
            plan_fromneighbor = np.matmul(agent_neighbor.p.T, self.subplans)

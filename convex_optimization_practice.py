from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict

def optimizeutility(agent, G, agentlist):
    print agent.idnum

    opt_prob = LpProblem("Optimize utility", LpMaximize)

    xs = [LpVariable("x{}".format(i+1), cat="Continuous") for i in range(len(agent.e))]

    # Objective function
    opt_prob += agent.u, "Optimization Function- agent utility"



    # add constraint
    total_spending = 0

    for nei in G.neighbors(agent.idnum):
        neighbor = agentlist[nei]
        print neighbor.e
        total_spending += np.dot(neighbor.p.T, xs)

    print total_spending
    opt_prob += total_spending <= agent.budget_constraint_ineq
    opt_prob += sum(xs) == agent.budget_constraint_eq

    opt_prob.solve()

    if opt_prob.status == LpStatusInfeasible:
            print "Constraints are infeasible!"

    if opt_prob.status == LpStatusUnbounded:
            print "Solution is unbounded!"

    if opt_prob.status == LpStatusOptimal:
            print "Optimal solution exists and is equal to: {} and the optimal point is:".format(value(opt_prob.objective))
            for variable in opt_prob.variables():
                    print "{} = {}".format(variable.name, variable.varValue)

G = nx.Graph()
G.add_edge(1,2)
c = 2
agentlist = defaultdict(Agent)
agent1 = Agent(1, 0, np.array((1,2)), np.array((1, 5)), np.array((0, 3)), np.array((0,0)), np.array((0,0)))
agentlist[1] = agent1

agent2 = Agent(1, 0, np.array((1,2)), np.array((1, 5)), np.array((0, 3)), np.array((0,0)), np.array((0,0)))
agentlist[2] = agent2

optimizeutility(agent1, G, agentlist)

from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict

def optimizelinearutility(agent, G, agentlist):
    num_goods = len(agent.e)
    opt_prob = LpProblem("Optimize utility", LpMaximize)

    xs = [LpVariable("x{}".format(i+1), cat="Continuous") for i in range(num_goods)]
    objective = np.dot(agent.u, np.array(xs))
    # Objective function
    opt_prob += objective, "Optimization Function- agent utility"

    # add constraint
    total_spending = 0

    for nei in G.neighbors(agent.idnum):
        neighbor = agentlist[nei]
        print (neighbor.e)
        total_spending += np.dot(neighbor.p.T, xs)

    print (total_spending )
    opt_prob += total_spending <= agent.budget_constraint_ineq
    #opt_prob += sum(xs) == agent.budget_constraint_eq

    for i in range(num_goods):
        opt_prob += xs[i] >= 0

    opt_prob.solve()

    if opt_prob.status == LpStatusInfeasible:
            print ("Constraints are infeasible!")

    if opt_prob.status == LpStatusUnbounded:
            print ("Solution is unbounded!")

    if opt_prob.status == LpStatusOptimal:
            print ("Optimal solution exists and is equal to: {} and the optimal point is:".format(value(opt_prob.objective)) )
            for variable in opt_prob.variables():
                    print ("{} = {}".format(variable.name, variable.varValue))

G = nx.Graph()
G.add_edge(1,2)
c = 2
agentlist = defaultdict(Agent)
#id num, utility, endowment, prices, subplans, r, k
agent1 = Agent(1, np.array((2,3)), np.array((300,100)), np.array((1, 5)), np.array([[0,0], [3,0]]), np.array((0,0)), np.array((0,0)))
agentlist[1] = agent1

agent2 = Agent(2, np.array((5,2)), np.array((100,200)), np.array((2, 5)), np.array([[0, 3], [0,0]]), np.array((0,0)), np.array((0,0)))
agentlist[2] = agent2

optimizelinearutility(agent1, G, agentlist)

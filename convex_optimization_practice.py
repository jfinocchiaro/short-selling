#from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict

def optimizelinearutility(agent, G, agentlist):
    num_goods = len(agent.e)
    opt_prob = LpProblem("Optimize utility", LpMaximize)
    num_neighbors = len(G.neighbors(agent.idnum))

    xs = [];
    for j in range(num_neighbors):
        xs.append([LpVariable("x{}".format(i+1+j*num_goods), cat="Continuous") for i in range(num_goods)]);

    print(np.array(xs))

    objective = np.sum(np.dot(np.array(xs), agent.u)) #symbolic

    print(objective)
    # Objective function
    opt_prob += objective, "Optimization Function- agent utility"

    # add constraint
    neighbor_prices = []
    total_spending = 0

    for j, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei]
        #print (neighbor.e)
        #neighbor_prices.extend(neighbor.p.T)
        total_spending += np.dot(neighbor.p.T, xs[j])

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


    total_goods_purchased = np.zeros((num_goods, 1))
    if opt_prob.status == LpStatusOptimal:
            print ("Optimal solution exists and is equal to: {} and the optimal point is:".format(value(opt_prob.objective)) )
            for count, variable in enumerate(opt_prob.variables()):
                    print ("{} = {}".format(variable.name, variable.varValue))
                    total_goods_purchased[(count % num_goods)] += variable.varValue

    print(total_goods_purchased)
    agent.r = np.multiply(agent.lambdafunc,total_goods_purchased) + agent.r

    return agent



G = nx.Graph()
G.add_edge(1,2)
G.add_edge(2,3)
c = 2
agentlist = defaultdict(Agent)
#id num, utility, endowment, prices, subplans, r, k
agent1 = Agent(1, np.array((10,1)), np.array((0,1)), np.array((10, 10)), np.array([[0,0], [3,0]]), np.array([0,1]))
agentlist[1] = agent1

agent2 = Agent(2, np.array((10,10)), np.array((0,0)), np.array((10,10)), np.array([[0, 3], [0,0]]), np.array([1, 1]))
agentlist[2] = agent2

agent3 = Agent(3, np.array((1,10)), np.array((1,0)), np.array((10,10)), np.array([[0,0], [3,0]]), np.array([1, 0]))
agentlist[3] = agent3


optimizelinearutility(agent2, G, agentlist)

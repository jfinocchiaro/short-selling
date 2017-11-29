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

    # xs is the subplan matrix of dimension n_neighbors * n_goods
    xs = [];
    for j in range(num_neighbors):
        xs.append([LpVariable("x{}".format(i+1+j*num_goods), cat="Continuous") for i in range(num_goods)]);

    # Use the xs matrix to compute the overall subplan for this agent. Sum
    # over the neighbor dimension for all the goods.

    subplan = np.sum(xs, axis=0);

    # We create optimization variables for the goods we want to keep.
    ks = [LpVariable("k{}".format(i+1), cat="Continuous") for i in range(num_goods)]

    # The rest is resold. This is a constraint in Elliott's document.
    rs = subplan - ks;

    print("subplan ", subplan);
    print("keep vector", ks);
    print("reselling vector", rs);

    print(np.array(ks).shape, agent.u.shape);
    # Maximize the u.k for this agent.
    objective = np.sum(np.dot(np.array(ks), agent.u)) #symbolic

    print("objective " + str(objective))
    # Objective function
    opt_prob += objective, "Optimization Function- agent utility"

    # add constraint
    neighbor_prices = []
    total_spending = 0

    for j, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei]
        #print (neighbor.e)
        #neighbor_prices.extend(neighbor.p.T)
        total_spending += np.dot(neighbor.p, np.array(xs[j]).T);

    print ("total_spending ", total_spending)

    # THe constraint for total spending is the endowment plus the resell gain.
    opt_prob += total_spending <= np.dot(agent.p, (agent.e + rs).T);
    #opt_prob += sum(xs) == agent.budget_constraint_eq

    # Each good bought should be a non-negative quantity.
    for n, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei];
        print("Neighbor %d " % (nei), " has endowment ", neighbor.e);
        for good in range(num_goods):
            opt_prob += xs[n][good] >= 0
            opt_prob += xs[n][good] <= neighbor.e[good];

    # The constraint on the goods kept is 0 < k_i < subplan_i;
    for i in range(num_goods):
        opt_prob += ks[i] >= 0;
        opt_prob += ks[i] <= subplan[i];

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

    sp = np.zeros((num_goods, 1))
    valvars = [val.varValue for val in opt_prob.variables()]

    for good in range(num_goods):
        for people in range(num_neighbors):
            sp[good] += float(valvars[good + ((people + 1) * num_goods)])


    #change this!
    agent.subplans = np.add(sp, agent.subplans)

    return agent


if __name__ == '__main__':
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

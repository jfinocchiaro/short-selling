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
    #rs = subplan - ks;

    print("subplan " + str(subplan));
    print("keep vector" + str(ks));

    # Maximize the u.k for this agent.
    objective = np.sum(np.dot(np.array(ks), agent.u)) #symbolic

    # Objective function
    opt_prob += objective, "Optimization Function- agent utility"

    # add constraint
    total_spending = 0

    for j, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei]
        total_spending += np.dot(neighbor.p, np.array(xs[j]).T);

    print ("total_spending ", total_spending) #symbolic

    # THe constraint for total spending is the endowment plus the resell gain.
    opt_prob += total_spending <= np.dot(agent.p, (agent.e + agent.resell).T);

    # Each good bought should be a non-negative quantity.
    for n, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei];
        print("Neighbor %d " % (nei) + " has endowment " + str(neighbor.e));
        for good in range(num_goods):
            opt_prob += xs[n][good] >= 0
            opt_prob += xs[n][good] <= neighbor.e[good] - neighbor.sellplan[good] + neighbor.resell[good];

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

    for people, neighbor in enumerate(G.neighbors(agent.idnum)):
        for good in range(num_goods):
            #need a way to reset sellplan for each iteration
            agentlist[neighbor].sellplan[good] += valvars[good + ((people + 1) * num_goods)]
            sp[good] += float(valvars[good + ((people + 1) * num_goods)])


    keep = valvars[:num_goods]
    print (keep)
    agent.subplans = sp #np.add(sp, agent.subplans)
    agent.resell = agent.subplans - keep
    print ('Reselling:\t' + str(agent.resell))
    #change this!

    return agent



G = nx.Graph()
G.add_edge(1,2)
G.add_edge(2,3)
c = 2
agentlist = defaultdict(Agent)
#id num, utility, endowment, prices, subplans
agent1 = Agent(1, np.array((10,1)), np.array((0,1)), np.array((10, 10)))
agentlist[1] = agent1

agent2 = Agent(2, np.array((10,10)), np.array((0,0)), np.array((10,10)))
agentlist[2] = agent2

agent3 = Agent(3, np.array((1,10)), np.array((1,0)), np.array((10,10)))
agentlist[3] = agent3


optimizelinearutility(agent2, G, agentlist)

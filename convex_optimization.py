#from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict

def optimizelinearutility(agent, G, agentlist):

    print ('Agent number %i' % agent.idnum)
    num_goods = len(agent.e)
    opt_prob = LpProblem("Optimize utility", LpMaximize)
    num_neighbors = len(G.neighbors(agent.idnum))
    # xs is the subplan matrix of dimension n_neighbors * n_goods
    xs = [];
    for j in range(num_neighbors):
        xs.append([LpVariable("x{}".format(i+1+j*num_goods), cat="Continuous") for i in range(num_goods)]);

    # Use the xs matrix to compute the overall subplan for this agent. Sum
    # over the neighbor dimension for all the goods.

    sub = np.sum(xs, axis=0);

    # We create optimization variables for the goods we want to keep.
    ks = [LpVariable("k{}".format(i+1), cat="Continuous") for i in range(num_goods)]

    # The rest is resold. This is a constraint in Elliott's document.
    rs = sub - ks;

    #print("sub " + str(sub));
    #print("keep vector" + str(ks));

    # Maximize the u.k for this agent.
    objective = np.sum(np.dot(np.array(ks), agent.u)) #symbolic

    # Objective function
    opt_prob += objective, "Optimization Function- agent utility"

    # add constraint
    total_spending = 0

    for j, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei]
        total_spending += np.dot(neighbor.p, np.array(xs[j]).T);

    print ("total_spending " +  str(total_spending)) #symbolic

    # THe constraint for total spending is the endowment plus the resell gain.
    opt_prob += total_spending <= np.dot(agent.p, (agent.e + rs).T);

    # Each good bought should be a non-negative quantity.
    for n, nei in enumerate(G.neighbors(agent.idnum)):
        neighbor = agentlist[nei];
        neighbor.e = neighbor.e.reshape(-1,1)
        print("Neighbor %d " % (nei) + " has endowment " + str(neighbor.e - neighbor.sellplan + neighbor.resell));
        for good in range(num_goods):
            opt_prob += xs[n][good] >= 0
            opt_prob += xs[n][good] <= neighbor.e[good] - neighbor.sellplan[good] + neighbor.resell[good];

    # The constraint on the goods kept is 0 < k_i < sub_i;
    for i in range(num_goods):
        opt_prob += ks[i] >= 0;
        opt_prob += ks[i] <= sub[i];

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
    keep = (np.array(keep).flatten().reshape(-1,1))
    agent.subplans = sp #np.add(sp, agent.subplans)
    agent.resell = (agent.subplans - np.array(keep))
    print ('Reselling:  ' + str(agent.resell))

    #change this!

    return agent

#from cvxopt import matrix, solvers
import agents
from agents import Agent
from pulp import *
import networkx as nx
import numpy as np
from collections import defaultdict
import dynamics
import makegraphs
import copy

LOAN_AMT = 1.0
LR = 0.02

def linearBuyGoods(ag, G, agentlist):
        agent = agentlist[ag]
        num_goods = len(agent.e)
        opt_prob = LpProblem("Optimize utility", LpMaximize)

        num_neighbors = len(G.neighbors(agent.idnum))

        # xs is the subplan matrix of dimension n_neighbors * n_goods
        xs = [];
        for j in range(num_neighbors):
            xs.append([LpVariable("x{}".format(i+1+j*num_goods), cat="Continuous") for i in range(num_goods)]);
        #cashmoney = (LpVariable("money", cat="Continuous"))

        # Use the xs matrix to compute the overall subplan for this agent. Sum
        # over the neighbor dimension for all the goods.

        subplan = np.sum(xs, axis=0);
        print 'subplan:  ' + str(subplan)

        # Maximize the u.k for this agent.
        objective = np.sum(np.dot(np.array(subplan), agent.u)) + agent.money #symbolic

        print("objective " + str(objective))
        # Objective function
        opt_prob += objective, "Optimization Function- agent utility"



        # add constraint
        #neighbor_prices = []
        total_spending = 0

        for j, nei in enumerate(G.neighbors(agent.idnum)):
            neighbor = agentlist[nei]
            #print (neighbor.e)
            #neighbor_prices.extend(neighbor.p.T)
            total_spending += np.dot(neighbor.p, np.array(xs[j]).T);

        #print ("total_spending ", total_spending)


        # THe constraint for total spending is the endowment plus the resell gain.
        opt_prob += total_spending <= min(np.dot(agent.p, (agent.e).T), agent.money);
        #opt_prob += sum(xs) == agent.budget_constraint_eq


        # Each good bought should be a non-negative quantity.
        for n, nei in enumerate(G.neighbors(agent.idnum)):
            neighbor = agentlist[nei];
            print("Neighbor %d " % (nei) + " has endowment "+ str(neighbor.e));
            for good in range(num_goods):
                opt_prob += xs[n][good] >= 0
                opt_prob += xs[n][good] <= neighbor.e[good];


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

        valvars = [val.varValue for val in opt_prob.variables()]



        print "Agent" + str(agent.idnum) + " endowment before: "+ str(agent.e)

        for people, nei in enumerate(G.neighbors(ag)):
            neighbor = agentlist[nei]
            #print "Neighbor " + str(nei) + " endowment before: " + str(neighbor.e)
            for good in range(num_goods):
                amt_bought = float(valvars[good + ((people) * num_goods)])
                amt_spent = float(amt_bought * neighbor.p[good])
                agent.e[good] += amt_bought
                neighbor.e[good] -= amt_bought
                agent.money -= amt_spent
                neighbor.money += amt_spent
            agentlist[nei] = neighbor
            #print "Neighbor " + str(nei) + " endowment after: " + str(neighbor.e)

        agentlist[ag] = agent
        print "Agent " + str(agent.idnum) + " endowment after: "  + str(agent.e)

        return agentlist


def buyGoods(ag, G, agentlist):
    #agent is idnumber of agent

    #endowmentplan is a buying plan

    agent = agentlist[ag]
    most_desired = [i[0] for i in sorted(enumerate(agent.u), reverse=True, key=lambda x:x[1])]
    print (most_desired)
    spending_money = np.dot(agent.endowmentplan, agent.p) + agent.money
    print 'Spending money:\t' + str(spending_money)
    for nei in G.neighbors(ag):
        neighbor = agentlist[nei]
        #COMMENCE THE TRADE
        for item in most_desired:
            while neighbor.endowmentplan[item] > 0 and spending_money > 0.01 * neighbor.p[item]:

                neighbor.endowmentplan[item] -= 0.01
                neighbor.money += 0.01 * neighbor.p[item]

                agent.endowmentplan[item] +=  0.01

                agent.money -= 0.01 * neighbor.p[item]

    print 'Agent endowment: \t' + str(agent.e) + '\tendowment plan:\t' + str(agent.endowmentplan)
    return agent

def changePlans(G,agentlist):
    for agent in G.nodes():
        agentlist = linearBuyGoods(agent, G, agentlist)

    for agent in G.nodes():
        #check_clear is set to the amount of items it plans to have after selling
        #agentlist[agent].check_clear = agentlist[agent].endowmentplan - agentlist[agent].e
        pass
    return agentlist

'''def checkClear(G, agentlist):
    for agent in G.nodes():
        if (agentlist[agent].money < LOAN_AMT):
            return False

    return True
'''

def adjustPrices(agentlist, num_rounds):

    for agent in agentlist.itervalues():
        money = agent.money

        print 'agent %i' % agent.idnum + ' money:  ' + str(money)
        print 'agent %i' % agent.idnum + ' prices:  ' + str(agent.p)
        num_goods = len(agent.p)
        if money < LOAN_AMT:
            for good in range(num_goods):
                agent.p[good] = np.round(max(agent.p[good] + LR  , 0.1), 2)
        elif money > LOAN_AMT:
            for good in range(num_goods):
                agent.p[good] = np.round(max(agent.p[good] - LR  , 0.1),2)


        agentlist[agent.idnum] = agent

        print 'agent %i' % agent.idnum + ' new prices:  ' + str(agent.p)



    return agentlist

'''
def adjustPrices(agentlist, check_clear):
    for agent in agentlist.itervalues():
        for i in range(agent.check_clear.shape[0]):
            if np.around(agent.check_clear[i], 2)  > 0:
                #prices too high
                agent.p[i] -= (agent.check_clear[i])
            elif np.around(agent.check_clear[i], 2) < 0:
                #prices too low
                agent.p[i] += (agent.check_clear[i])
        agentlist[agent.idnum] = agent
    return agentlist
'''

def checkTradeHappen(agents_old, agents_new):
    print (agents_old[1].e == agents_new[1].e)

    for ag in agents_old.iterkeys():
        print agents_old[ag].e
        print agents_new[ag].e
        if (agents_old[ag].e == agents_new[ag].e).all():
            pass
        else:
            return True
    return False

def budgetCheck(G, agentlist, round_num):
    cap = 0
    for agent in agentlist.itervalues():
        cap += agent.money

    for agent in agentlist.itervalues():
        neighbor_moneys = [agentlist[x].money for x in G.neighbors(agent.idnum)]
        rni = neighbor_moneys.index(max(neighbor_moneys))
        richest_nei = G.neighbors(agent.idnum)[rni]

        rich_neighbor = agentlist[richest_nei]
        if all(agent.p > cap) and all(rich_neighbor.e == 0) and round_num > 0:
            return True

    return False

def startEconomy(G,agentlist):
    check_clear = False
    trade = True
    budget_cap = False
    num_rounds = 0
    while (budget_cap == False) and (trade == True) or num_rounds < 3:
    #while (check_clear == False):
        print 'Round num %i' % num_rounds
        agents_old = copy.deepcopy(nx.get_node_attributes(G, 'agentprop'));
        #agentlist = nx.get_node_attributes(G, 'agentprop')
        agents_new = changePlans(G, agents_old)
        agents_new = adjustPrices(agents_new, num_rounds)
        trade = checkTradeHappen(agents_old, agents_new)
        #check_clear = checkClear(G, agents_new)
        budget_cap = budgetCheck(G, agents_new, num_rounds)

        nx.set_node_attributes(G, 'agentprop', agents_new)
        num_rounds += 1
        print 'Trade: ' + str(trade)
        print 'BC:  ' + str(budget_cap)


    print('Rounds played:  '+ str(num_rounds))

    return G


if __name__ == '__main__':
    G = makegraphs.ec_toy()
    c = 2
    agentlist = defaultdict(Agent)
    #id num, utility, endowment, prices, subplans,

    #middlemen.  Agent 1 degree central, agent 2 between central
    
    agentlist[2] = Agent(2, np.array((10,1)), np.array((0.01,0.98)), np.array((10, 10)), loan=LOAN_AMT)
    agentlist[1] = Agent(1, np.array((10,10)), np.array((0.01,0.01)), np.array((10,10)), loan=LOAN_AMT)

    #type 1 util player
    agentlist[3] = Agent(3, np.array((1,10)), np.array((0.98,0.01)), np.array((1,10)), loan=LOAN_AMT)
    agentlist[6] = Agent(6, np.array((1,10)), np.array((0.98,0.01)), np.array((1,10)), loan=LOAN_AMT)

    #type 2 util player
    agentlist[4] =  Agent(4, np.array((10,10)), np.array((0.01,0.01)), np.array((10,10)), loan=LOAN_AMT)
    agentlist[5] =  Agent(5, np.array((1,10)), np.array((0.98,0.01)), np.array((1,10)), loan=LOAN_AMT)

    #only connected to 2
    agentlist[7] = Agent(7, np.array((5,5)), np.array((0.5,0.5)), np.array((5,5)), loan=LOAN_AMT)


    nx.set_node_attributes(G, 'agentprop', agentlist)
    G = startEconomy(G, agentlist)
    dynamics.drawFNetwork(G, 'agentprop', 'frenchtoy.png')

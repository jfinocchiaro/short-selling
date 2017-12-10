import networkx as nx
import numpy as np
import makegraphs
from agents import Agent
from collections import defaultdict
import dynamics
from pulp import *
import copy

NUM_AGENTS = 3
NUM_GOODS = 2
LR = 0.1

#use pulp to perform a linear optimization to buy goods
def linearBuyGoods(G, agentlist):
    #every agent buys goods
    for agent in agentlist.values():

        #define the optimization problem.  Should be maximizing agents u(x) subject to neighbors endowment
        #x is what they are buying
        #endowment is what they have
        opt_prob = LpProblem("Optimize utility", LpMaximize)

        num_neighbors = len(G.neighbors(agent.idnum))

        A = [];
        for j in range(num_neighbors):
            A.append([LpVariable("x{}".format(i+1+j*NUM_GOODS), cat="Continuous") for i in range(NUM_GOODS)]);

        #objective is to maximize the utility of what the agent plays to buy
        objective = np.sum(np.dot(np.sum(A, axis=0), agent.u)) #symbolic

        #add the objective function to the optimization problem
        opt_prob += objective, "What we actually aim to optimize"

        #starting budget constraint is how much they would have if they sold everything with their current price vector
        budget = np.dot(agent.p, agent.e)

        #buy_plan is a list of the costs of each good
        buy_plan = []

        #subject to what their neighbors have to sell
        for count, nei in enumerate(G.neighbors(agent.idnum)):
            #neighbor is the Agent item instead of the index in the dict
            neighbor = agentlist[nei]

            #a player cannot buy more than what a neighbor owns
            for item in range(NUM_GOODS):
                #how much an agent buys from a neighbor is restricted to how much the neighbor owns
                opt_prob += np.dot(neighbor.p[item], A[count][item]) <= neighbor.e[item]

                #must buy a non negative amount of a good
                opt_prob += A[count][item] >= 0

                #add the price per unit to the buy_plan so that the sum is restricted to the player's budget
                buy_plan.append(np.dot(neighbor.p[item], A[count][item]))

        #how much the agent spends is restricted to their current budget, calculated from their endowment and current prices
        opt_prob += np.sum(buy_plan) <= budget

        opt_prob.solve()

        #If the feasible region is empty i.e. no trade happens
        if opt_prob.status == LpStatusInfeasible:
                print ("Constraints are infeasible!")

                for nei in G.neighbors(agent.idnum):
                    agent.x[nei] = [0] * NUM_GOODS


        #If the feasible region is unbounded in the direction of optimization
        if opt_prob.status == LpStatusUnbounded:
                print ("Solution is unbounded!")
                #uh oh

                for nei in G.neighbors(agent.idnum):
                    agent.x[nei] = [0] * NUM_GOODS



        #if there is a feasible optimal point
        if opt_prob.status == LpStatusOptimal:
            #print ("Optimal solution exists and is equal to: {} and the optimal point is:".format(value(opt_prob.objective)) )
            #for count, variable in enumerate(opt_prob.variables()):
                    #print ("{} = {}".format(variable.name, variable.varValue))

            #this next section only happens if there is an optimal solution
            #list of the optimized values
            optimal_values = [val.varValue for val in opt_prob.variables()]

            agent.bought_items = [0]* NUM_GOODS


            #adjust agents x value
            counter = 0 #iterates through optimal_values
            for nei in G.neighbors(agent.idnum):

                #add bought_items and demand properties to agent
                neighbor = agentlist[nei]


                #agent.x[neigh] is [list of items bought from neigh]
                for i in range(NUM_GOODS):
                    if len(agent.x[nei]) < NUM_GOODS:
                        agent.x[nei].append(optimal_values[counter])
                    else:
                        #add property to agent's bought items
                        agent.x[nei][i] = (optimal_values[counter])

                    neighbor.demand[i] += optimal_values[counter]
                    agent.bought_items[i] += optimal_values[counter]

                    counter += 1



                #adjust the neighbor (with new demand) in the agentlist
                agentlist[nei] = neighbor


            #end if an optimal solution

        agentlist[agent.idnum] = agent



    return agentlist



#reset the market to the initial endowments in order to re-simulate at different prices
#DONE
def resetMarket(G, initial_agentlist, agentlist):
    #nx.set_node_attributes(G, 'agentprop', initial_agentlist)
    #agentlist = copy.deepcopy(initial_agentlist)
    for agent in agentlist.values():
        agent.x = initial_agentlist[agent.idnum].x
        agent.e = np.round(initial_agentlist[agent.idnum].e,2)
        agent.demand = initial_agentlist[agent.idnum].demand
        agent.bought_items = initial_agentlist[agent.idnum].bought_items

        agentlist[agent.idnum] = agent

    return agentlist


#we say the local market clears if the demand for an agents endowment is equal to the supply
#DONE
def checkMarketClearance(agentlist, G):
    #return a dict containing lists of 0s and 1s of where ret[i] = 0 if agent i's market has cleared and 1 oversell and -1 if undersell
    keys = agentlist.keys()
    mkt_clear = {key: [] for key in keys}
    pos_endows = True
    #iterate over every agent in the market
    for agent in agentlist.values():
        #check if every good has sold
        for good in range(NUM_GOODS):
            #calculate supply from e
            supply = np.round(agent.e[good])
            demand = np.round(agent.demand[good],1)
            #market for this item clears
            if supply == demand:

                if len(mkt_clear[agent.idnum]) < NUM_GOODS:
                    mkt_clear[agent.idnum].append(0)
                else:
                    mkt_clear[agent.idnum][good] = 0

            #item undersells
            elif supply > demand:
                if len(mkt_clear[agent.idnum]) < NUM_GOODS:
                    mkt_clear[agent.idnum].append(-1)
                else:
                    mkt_clear[agent.idnum][good] = -1

            #item oversells
            else:
                pos_endows = False
                if len(mkt_clear[agent.idnum]) < NUM_GOODS:
                    mkt_clear[agent.idnum].append(1)
                else:
                    mkt_clear[agent.idnum][good] = 1





    return mkt_clear, pos_endows


def checkTradeHappened(agentlist, G, prev_agents):
    #if any has a nonzero x, trade happened
    #agent.x is a dict of lists where agent.x[person_id] is a list of the items agent bought from person

    for agent in agentlist.values():
        #print 'previous endowment:  %s \t current endowment %s' % (prev_agents[agent.idnum].e, agent.e)

        if any(agent.e != prev_agents[agent.idnum].e):

            return True
        else:
            pass

    #print ('No trade happened')
    return False

#once we have each agent's plan to trade actually go through with the trade
def commenceTrade(agentlist):
    for agent in agentlist.values():
        #new endowment is what they previously had plus what they bought minus what they sold
        #print ('Agent %s endowment:  %s\t demand on items:  %s\titems to buy %s' % (agent.idnum, agent.e, agent.demand, agent.bought_items))
        agent.e = np.round(np.subtract(np.add(agent.e, agent.bought_items), agent.demand),2)


        agent.bought_items = [0] * NUM_GOODS
        agent.demand = [0] * NUM_GOODS
        agentlist[agent.idnum] = agent



    return agentlist

#imagine gradient descent for prices
#DONE
def adjustPrices(agentlist, mkt_clear):
    for agent in agentlist.values():
        #delta is a rough derivative just in the sense that its the rate of change (change over unit time)
        delta = np.subtract(agent.e, agent.demand)

        #GRADIENT DESCENT: a_(n+1) = a_n - LR * delta
        agent.p = [max(agent.p[i] + (LR*delta[i]), 0) for i in range(NUM_GOODS)]

        #update agentlist
        agentlist[agent.idnum] = agent

    #end for each agent in the network


    #return the agentlist with new prices
    return agentlist



def main():
    #true while there is still trade happening in the network
    still_trading = True

    #loaded in from Varad's function
    #G = makegraphs.starGraph(3) #CHANGE
    G = nx.Graph()
    G.add_edge(1,2)
    G.add_edge(1,3)

    #should be a dict of agents so when we need to reset the market after adjusting prices we set it to this
    initial_agentlist = defaultdict(Agent) #CHANGE
    #idnum, utility, endowment,  prices
    initial_agentlist[1] = Agent(1, np.array((10,10)), np.array((1,1)), np.array((10,10)))
    initial_agentlist[2] = Agent(2, np.array((1,10)), np.array((10,1)), np.array((10,1)))
    initial_agentlist[3] = Agent(3, np.array((10,1)), np.array((1,10)), np.array((1,10)))

    #this dict gets changed as trade happens
    agentlist = copy.deepcopy(initial_agentlist)

    #all non-zero until a player's local market clears
    keys = agentlist.keys()
    mkt_clear = {key:([1]*NUM_GOODS) for key in keys}
    #all_clear = [mkt_clear[i] == ([0] * NUM_GOODS) for i in mkt_clear.keys()]
    all_clear = False


    demand = 1
    pos_endows = True
    rounds_of_trading = 2

    #while(1):
    while not (all_clear) and rounds_of_trading > 1:
        #trade is still happening since markets haven't cleared

        #counter for the total number of rounds trade happens at the current prices
        j = 0
        still_trading = True

        while (demand > 0) and pos_endows and still_trading:
            prev_agents = copy.deepcopy(agentlist)

            #plan trade
            agentlist = linearBuyGoods(G, agentlist)

            #grab the demand from this round
            demand_list = [i.demand for i in agentlist.values()]
            flat_list = [item for sublist in demand_list for item in sublist]

            demand = max(flat_list)



            endows_list = [i.e for i in agentlist.values()]
            flat_list = [item for sublist in endows_list for item in sublist]
            if min (flat_list) <= 0:
                pos_endows = False
            else:
                pos_endows = True
                #commence the trade!
                agentlist = commenceTrade(agentlist)



            still_trading = checkTradeHappened(agentlist, G, prev_agents)


            j += 1

        rounds_of_trading = j
        #end while (still_trading == True)


        #check if the market cleared
        mkt_clear, pos_endows = checkMarketClearance(agentlist, G)

        all_clear = True

        for i in mkt_clear.values():
            for j in range(len(i)):
                if j != 0:
                    all_clear = False

        #list of booleans for each agent's local market failing to clear
        #all_clear = [all(mkt_clear[i] == ([0] * NUM_GOODS)) for i in mkt_clear.values()]


        #re-run the simulation with different prices
        if not (all_clear):
            ##save the previous prices before resetting the market

            #reset the market
            agentlist = resetMarket(G, initial_agentlist, agentlist)

            #adjust the prices each player sells at
            agentlist = adjustPrices(agentlist, mkt_clear)



        #end if the market has not completely cleared
    #end while the market has not completely cleared

    #print prices
    for agent in agentlist.values():
        print ('Agent %i prices:  %s\t endowment:  %s' % (agent.idnum, agent.p, agent.e))
    #save image to a file
    nx.set_node_attributes(G, 'agentprop', agentlist)
    dynamics.drawFNetwork(G, 'agentprop', 'frenchsplit.png')


if __name__ == '__main__':
    main()

import networkx as nx
import numpy as np
import makegraphs
from agents import Agent
from collections import defaultdict
import dynamics

NUM_AGENTS = 3
NUM_GOODS = 2
LR = 0.1

#use pulp to perform a linear optimization to buy goods
def linearBuyGoods(G, agentlist):
    #TODO
    pass


#reset the market to the initial endowments in order to re-simulate at different prices
#DONE
def resetMarket(G, initial_agentlist):
    nx.set_node_attributes(G, 'agentprop', initial_agentlist)
    return initial_agentlist


#we say the local market clears if the demand for an agents endowment is equal to the supply
#DONE
def checkMarketClearance(agentlist, G):
    #return a dict containing lists of 0s and 1s of where ret[i] = 0 if agent i's market has cleared and 1 oversell and -1 if undersell
    keys = agentlist.keys()
    mkt_clear = {key: [] for key in keys}
    #iterate over every agent in the market
    for agent in agentlist.values():
        #check if every good has sold
        for good in range(NUM_GOODS):
            #calculate supply from e
            supply = agent.e[good]

            #calculate demand from sum over its neighbors buying plans (buying plan should be a dict?)
            demand = 0
            for nei in G.neighbors(agent.idnum):
                neighbor = agentlist[nei]
                #buy_vector is buying plan AKA what this neighbor plans to buy from this specific player
                demand += neighbor.x[agent.idnum][good]

            agent.demand[good] = demand
            #market for this item clears
            if supply == demand:
                mkt_clear[agent.idnum].append(0)

            #item undersells
            elif supply > demand:
                mkt_clear[agent.idnum].append(-1)

            #item oversells
            else:
                mkt_clear[agent.idnum].append(1)


    return mkt_clear


def checkTradeHappened(agentlist, G):
    #if any has a nonzero x, trade happened
    #agent.x is a dict of lists where agent.x[person_id] is a list of the items agent bought from person
    for agent in agentlist.values():
        #iterate over all of agent's neighbors
        for nei in G.neighbors(agent.idnum):
            print(agent.x[nei])
            if (agent.x[nei] != ([0]*NUM_GOODS)):
                return True
            else:
                pass

    return False

#imagine gradient descent for prices
#DONE
def adjustPrices(agentlist, mkt_clear):
    #delta is a rough derivative just in the sense that its the rate of change (change over unit time)
    delta = np.subtract(agent.e, agent.demand)

    #GRADIENT DESCENT: a_(n+1) = a_n - LR * delta

    #for every player in the ecenomy
    for player in mkt_clear.keys():
        agent = agentlist[player]
        for good in range(len(player)):
            #if their market has not cleared ie mkt_clear[player] == 0
            if mkt_clear[player][good] == 0:
                #item has cleared
                pass
            elif mkt_clear[player][good] > 0:
                #item has oversold
                agent.p[good] = agent.p[good] - (LR * delta)
            else:
                #item has undersold
                agent.p[good] = agent.p[good] - (LR * delta)

        agentlist[player] = agent


    #return the agentlist with new prices
    return agentlist



def main():
    #true while there is still trade happening in the network
    still_trading = True

    #loaded in from Varad's function
    G = makegraphs.starGraph(3) #CHANGE
    G.add_edge(1,2)
    G.add_edge(2,3)

    #should be a dict of agents so when we need to reset the market after adjusting prices we set it to this
    initial_agentlist = defaultdict(Agent) #CHANGE
    initial_agentlist[1] = Agent(1, np.array((1,1)), np.array((1,1)), np.array((1,1)))
    initial_agentlist[2] = Agent(2, np.array((1,1)), np.array((1,1)), np.array((1,1)))
    initial_agentlist[3] = Agent(3, np.array((1,1)), np.array((1,1)), np.array((1,1)))

    #this dict gets changed as trade happens
    agentlist = initial_agentlist

    #all non-zero until a player's local market clears
    keys = agentlist.keys()
    mkt_clear = {key:([1]*NUM_GOODS) for key in keys}


    while (mkt_clear.values() != ([[0] * NUM_GOODS] * NUM_AGENTS)):
        #trade is still happening since markets haven't cleared
        still_trading = True
        while (still_trading == True):
            #commence buys



            #TODO: Debug here.  Agentlist returns a dict with 3 null entries in elements 1, 2 and 3 Don't know why it's iterating farther but it's saying there are 7 elements in agentlist.  maybe its a cache thing
            for agent in agentlist.values():
                #commence buying
                agentlist[agent] = linearBuyGoods(G, agentlist)


            still_trading = checkTradeHappened(agentlist, G)
        #end while (still_trading == True)


        #check if the market cleared
        mkt_clear = checkMarketClearance(agentlist, G)

        #re-run the simulation with different prices
        if (((mkt_clear != ([0] * NUM_GOODS)).all()).all()):
            #adjust the prices each player sells at
            agentlist = adjustPrices(agentlist, mkt_clear)
            #reset the market
            agentlist = resetMarket(initial_agentlist)

        #end if the market has not completely cleared
    #end while the market has not completely cleared

    #print prices
    for agent in agentlist.values():
        print ('Agent %i prices:  %s' % (agent.idnum, agent.p))
    #save image to a file
    dynamics.drawFNetwork(G, 'agentprop', 'frenchsplit.png')


if __name__ == '__main__':
    main()

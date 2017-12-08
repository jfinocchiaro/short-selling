import agents
import networkx as nx
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

def process_centrulity(G, num_types):
    agentlist = nx.get_node_attributes(G, 'agentprop')
    
    #final_utility = [agentlist[node].calcUtility() for node in G.nodes()];
    dc = nx.degree_centrality(G);
    bc = nx.degree_centrality(G);

    dcent = {};
    bcent = {};
    final_utility = {};

     
    for config in range(num_types):
        dcent[config] = [];
        bcent[config] = [];
        final_utility[config] = [];
        print(config);
        for node in G.nodes():
            agent = agentlist[node];
            if agent.type == config:
                final_utility[config].append(agent.calcUtility())# - agent.u_init); 
	        dcent[config].append(dc[node]);
	        bcent[config].append(bc[node]);
      
	final_utility[config] = np.array(final_utility[config]);
	dcent[config] = np.array(dcent[config]);
	bcent[config] = np.array(bcent[config]);
	idx = np.argsort(-final_utility[config]);

        final_utility[config] = final_utility[config][idx];
	dcent[config] = dcent[config][idx]
        bcent[config] = bcent[config][idx]

	plt.plot(dcent[config], final_utility[config], '.', label='%d' % (config));

	print(dcent[config]);
	print(bcent[config]);
	print(final_utility[config]);
    
        plt.legend();
        plt.savefig('centrulity_%d.png' % (config));
	plt.gcf().clear()


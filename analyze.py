import agents
import networkx as nx
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

def process_centrulity(G, num_types):
    agentlist = nx.get_node_attributes(G, 'agentprop')
    
    #final_utility = [agentlist[node].calcUtility() for node in G.nodes()];
    dc = nx.degree_centrality(G);
    bc = nx.betweenness_centrality(G);

    dcent = {};
    bcent = {};
    final_utility = {};

    np.set_printoptions(precision=2) 
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
	
	for node in G.nodes():
	    if agentlist[node].type == config:
	       agent = agentlist[node];
	       plt.title('Utility ' + str(agent.u) + ', Endowment ' + str(agent.e_init)); 
	       break;
      
	final_utility[config] = np.array(final_utility[config]);
	dcent[config] = np.array(dcent[config]);
	bcent[config] = np.array(bcent[config]);
	idx = np.argsort(-final_utility[config]);

        final_utility[config] = final_utility[config][idx];
	dcent[config] = dcent[config][idx]
        bcent[config] = bcent[config][idx]

	plt.plot(dcent[config], '.', label='degree centrality');
	plt.plot(bcent[config], '.', label='betweenness centrality');
	plt.plot(normalize(final_utility[config]), '.', label='utility');

	print(dcent[config]);
	print(bcent[config]);
	print(final_utility[config]);
    
        plt.legend();
        plt.savefig('centrulity_%d.png' % (config));
	plt.gcf().clear()


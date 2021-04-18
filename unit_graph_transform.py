import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


G = nx.read_gpickle('output/graph.gpickle')
source_node = list(G.nodes())[0]
sink_node = list(G.nodes())[-1]

H = nx.DiGraph()

for ind, node in enumerate(G.nodes(data=True)):
    ind = ind + 1
    print(ind, G.nodes[ind])
    rank = G.nodes[ind]['rank']
    color = G.nodes[ind]['color']
    weight = G.nodes[ind]['weight']
    preds = list(G.predecessors(ind))
    succs = list(G.successors(ind))
    if ind == source_node:
        H.add_node(source_node, color=color, rank=rank, weight=weight)
        continue
    if ind == sink_node:
        H.add_node(sink_node, color=color, rank=rank, weight=weight)
    else:
        for ii in range(1,weight+1):
            H.add_node(f'{ind},{ii}', color=color,rank=rank,weight=1)
        for ii in range(2,weight+1):
            H.add_edge(f'{ind},{ii-1}',f'{ind},{ii}')
    for pred in preds:
        if pred == source_node:
            H.add_edge(source_node, f'{ind},1')
        elif ind == sink_node:
            last = G.nodes[pred]['weight']
            H.add_edge(f'{pred},{last}',sink_node)
        else:
            last = G.nodes[pred]['weight']
            H.add_edge(f'{pred},{last}',f'{ind},1')
last = G.nodes[ind-1]['weight']
H.add_edge(f'{ind-1},{last}',sink_node)

color_map=[]
pos = nx.spring_layout(H, seed=5, k=0.7*1/np.sqrt(len(H.nodes())), iterations=20)
attr_list=H.nodes(data='color')
for attr in attr_list:
    color_map.append(attr[1])
nx.draw_networkx(H,pos,with_labels=True, node_color=color_map, node_size=500)
plt.savefig('output/unit_graph.png')
plt.show()
nx.write_gpickle(H,'output/unit_graph.gpickle')


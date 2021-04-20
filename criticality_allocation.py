import networkx as nx
import pickle
from crit_set_class import criticality_set

class path:
    def __init__(self, node_list, path_len):
        self.node_list = node_list
        self.path_len = path_len 

def criticality_allocate(start_node, end_node, path, completed):
    start_crit_set = G.nodes[start_node]['crit_set']
    end_crit_set = G.nodes[end_node]['crit_set']
    num_crit_set = end_crit_set - start_crit_set - 1
    start_pos = path.index(start_node)
    end_pos = path.index(end_node)
    num_nodes = end_pos - start_pos - 1
    f = (int)(num_crit_set / num_nodes)
    g = num_crit_set % num_nodes
    lower_bound = start_crit_set
    upper_bound = lower_bound
    cur_pos = path.index(start_node) + 1
    end_pos = path.index(end_node)
    while cur_pos < end_pos:
        cur_node = path[cur_pos]
        lower_bound = upper_bound + 1
        upper_bound = lower_bound + f - 1
        if cur_pos >= path.index(end_node) - g:
            upper_bound = lower_bound + f
        cur_node_color = G.nodes[cur_node]['color']
        best_set = lower_bound
        if cur_node_color == 'green':
            best_time = crit_set_list[best_set].green_time
        else:
            best_time = crit_set_list[best_set].red_time
        for ind in range(lower_bound, upper_bound + 1):
            if cur_node_color == 'green':
                time = crit_set_list[ind].green_time
            else:
                time = crit_set_list[ind].red_time
            if ind != best_set and time < best_time:
                best_set = ind
                best_time = time
        G.nodes[cur_node]['crit_set'] = best_set
        crit_set_list[best_set].add_node(cur_node, G.nodes[cur_node]['color'], G.nodes[cur_node]['weight'])
        completed.append(cur_node)
        cur_pos = cur_pos + 1

paths = []
G = nx.read_gpickle('output/unit_graph.gpickle')
source_node = list(G.nodes())[0]
sink_node = list(G.nodes())[-1]
G = nx.relabel_nodes(G,{source_node:str(source_node), sink_node:str(sink_node)})
source_node = str(source_node)
sink_node = str(sink_node)
path_list = nx.all_simple_paths(G,source=source_node,target=sink_node)


for walk in path_list:
    path_length = 0
    for node in walk:
        path_length = path_length + G.nodes[node]['weight']
    new_path = path(walk, path_length)
    paths.append(new_path)


ordered_paths = sorted(paths, key=lambda x:x.path_len, reverse=True)
lmax = ordered_paths[0]
completed = []

crit_set_list = []

G.nodes[source_node]['crit_set'] = 0
completed.append(source_node)
end_set =  lmax.path_len - G.nodes[source_node]['weight'] - G.nodes[sink_node]['weight'] + 1
G.nodes[sink_node]['crit_set'] = end_set

for ind in range(0,end_set + 1):
    crit_set_list.append(criticality_set())

crit_set_list[0].add_node(source_node, G.nodes[source_node]['color'], G.nodes[source_node]['weight'])
crit_set_list[end_set].add_node(sink_node, G.nodes[sink_node]['color'], G.nodes[sink_node]['weight'])



ind = 1
for node in lmax.node_list:
    if node == source_node or node == sink_node:
        continue
    G.nodes[node]['crit_set'] = ind
    crit_set_list[ind].add_node(node, G.nodes[node]['color'], G.nodes[node]['weight'])
    completed.append(node)
    ind = ind + 1
completed.append(sink_node)

for ii in range(1,len(ordered_paths)):
    l = ordered_paths[ii]
    M = []
    for node in l.node_list:
        if node in completed:
            M.append(node)
    if set(M) == set(l.node_list):
        continue
    M_len = len(M)
    pos = 0
    while pos < M_len - 1:
        cur_node = M[pos]
        next_node = M[pos+1]
        difference = l.node_list.index(next_node) - l.node_list.index(cur_node)
        if difference != 1:
            criticality_allocate(cur_node, next_node, l.node_list, completed)
        pos = pos + 1

nx.write_gpickle(G,'output/criticality_allocated_graph.gpickle')
with open('output/criticality_set_allocation.pkl', 'wb') as outfile:
    pickle.dump(crit_set_list, outfile)
import pickle
import networkx as nx
import json
import pandas as pd

def inf_fn(crit_set):
    num_green = -1
    num_red = -1
    for node in crit_set.node_list:
        color = G.nodes[node]['color']
        if color == 'green':
            num_green = num_green + 1
        else:
            num_red = num_red + 1
    green_block = num_green/config['green']
    red_block = num_red/config['red']
    return max(green_block,red_block)

def vol_fn():
    node_list = G.nodes(data=True)
    green_vol = 0
    red_vol = 0
    for node in node_list:
        values = node[1]
        weight = values['weight']
        if values['color'] == 'green':
            green_vol = green_vol + weight
        else:
            red_vol = red_vol + weight
    red_vol = red_vol/config['red']
    green_vol = green_vol/config['green']
    total_vol = red_vol + green_vol
    return total_vol

def jeffery_fn():
    total_vol = vol_fn()
    max_color = max(config['green'],config['red'])
    wcrt = config['Max Length'] + total_vol - (config['Max Length']/max_color)
    return wcrt


def base_fn():
    base_wcrt = 0
    for idx, crit_set in enumerate(crit_set_list):
        if idx == 0 or idx == len(crit_set_list) - 1:
            continue
        wcrt = inf_fn(crit_set)
        crit_set.wcrt = wcrt
        base_wcrt = base_wcrt + wcrt
    base_wcrt = base_wcrt + config['Max Length']
    return base_wcrt

def han_fn():
    total_vol = vol_fn()
    total_block = []
    path_list = nx.all_simple_paths(G,source=config["source"],target=config["sink"])
    for path in path_list:
        total_block.append(r_prime(path))
    max_block = max(total_block)
    wcrt = total_vol + max_block
    return wcrt

def r_prime(node_list):
    path_len = 0
    green_block = 0
    red_block = 0
    for node in node_list:
        weight = G.nodes[node]['weight']
        color = G.nodes[node]['color']
        path_len = path_len + weight
        if color == 'green':
            green_block = green_block + weight/config['green']
        else:
            red_block = red_block + weight/config['red']
    return path_len - green_block - red_block

G = nx.read_gpickle('output/criticality_allocated_graph.gpickle')
H = nx.read_gpickle('output/graph.gpickle')
with open('output/criticality_set_allocation.pkl', 'rb') as infile:
    try:
        crit_set_list = pickle.load(infile)
    except pickle.PicklingError as e:
        print('Got pickling error'.format(e))


with open('config.json') as infile:
    config = json.load(infile)

result_file = 'output/results.csv'
try:
    df = pd.read_csv(result_file,index_col=0)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Number of Nodes','Jeffery','Han','Base Paper','Actual','Improvement in Percent'])
    df.to_csv(result_file, index=None)
    df = pd.read_csv(result_file)

jeffery_wcrt = jeffery_fn()
han_wcrt = han_fn()
base_wcrt = base_fn()
actual = config['Response Time']
num_nodes = len(H.nodes())
improvement = (jeffery_wcrt - actual)/jeffery_wcrt * 100
wcrt_dict = {"Number of Nodes":num_nodes,"Jeffery":jeffery_wcrt,"Han":han_wcrt,"Base Paper":base_wcrt,"Actual":actual,"Improvement in Percent":improvement}
ndf = pd.DataFrame.from_records([wcrt_dict])
cdf = pd.concat([df,ndf], ignore_index=True)
print(cdf)
cdf.to_csv(result_file)
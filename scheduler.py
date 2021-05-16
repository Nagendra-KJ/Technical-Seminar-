import pickle
import networkx as nx
import json


class core:
    def __init__(self, color):
        self.color = color
        self.idle = True
        self.task = None
    
    def update_core(self):
        global num_idle_green_cores,num_idle_red_cores
        if self.task == None:
            return
        if G.nodes[self.task]['start_time'] + G.nodes[self.task]['weight'] <= time:
            task_completed = self.task
            self.task = None
            self.idle = True
            if self.color == 'green':
                num_idle_green_cores = num_idle_green_cores + 1
            else:
                num_idle_red_cores = num_idle_red_cores + 1
            return task_completed
        return
    
    def assign_task(self, task):
        global num_idle_green_cores,num_idle_red_cores
        self.idle = False
        self.task = task
        G.nodes[task]['start_time'] = time
        G.nodes[task]['core'] 
        if self.color == 'green':
            num_idle_green_cores = num_idle_green_cores - 1
        else:
            num_idle_red_cores = num_idle_red_cores - 1
            
            


def find_idle(color):
    for ind, core in enumerate(core_list):
        if core.idle == True and core.color == color:
            return ind
    return -1

def check_preds_done(preds):
    if len(preds) == 0:
        return True
    for pred in preds:
        if G.nodes[pred]['executed'] == False:
            return False
    return True

G = nx.read_gpickle('output/criticality_allocated_graph.gpickle')
with open('output/criticality_set_allocation.pkl', 'rb') as infile:
    try:
        crit_set_list = pickle.load(infile)
    except pickle.PicklingError as e:
        print('Got pickling error'.format(e))

with open('config.json') as infile:
    config = json.load(infile)


num_green_cores = input('Enter the number of green cores available:')
num_red_cores = input('Enter the number of red cores available:')

num_green_cores = int(num_green_cores)
num_red_cores = int(num_red_cores)



num_idle_green_cores = num_green_cores
num_idle_red_cores = num_red_cores

core_list = []

for ind in range(num_green_cores):
    core_list.append(core('green'))

for ind in range(num_red_cores):
    core_list.append(core('red'))



for node in G.nodes():
    G.nodes[node]['executed'] = False
    G.nodes[node]['start_time'] = None
    G.nodes[node]['core'] = None
    G.nodes[node]['end_time'] = None

source_node = list(G.nodes())[0]

task_queue = []
completed = []
time = 0

task_queue.append(source_node)
cur_node = None

while len(completed) != len(G.nodes()):
    if num_idle_green_cores > 0 or num_idle_red_cores > 0:
        for task in task_queue:
            if G.nodes[task]['start_time'] == None:
                task_weight = G.nodes[task]['weight']
                task_color = G.nodes[task]['color']
                idle_core = find_idle(task_color)
                preds = list(G.predecessors(task))
                preds_done = check_preds_done(preds)
                if idle_core > -1 and preds_done:
                    core_list[idle_core].assign_task(task)
                    G.nodes[task]['core'] = idle_core
    time = time + 1
    for core in core_list:
        task_completed = core.update_core()
        if task_completed != None:
            completed.append(task_completed)
            G.nodes[task_completed]['end_time'] = time
            G.nodes[task_completed]['executed'] = True
            succs = list(G.successors(task_completed))
            task_queue.remove(task_completed)
            task_queue.extend(succs)
            

nx.write_gpickle(G,'output/time_allocated_graph.gpickle')
with open('config.json','w') as outfile:
    config['green'] = num_green_cores
    config['red'] = num_red_cores
    config['Response Time'] = time
    json.dump(config,outfile)
        
    
    
    
    
    
    
    
    
    
    
    
    




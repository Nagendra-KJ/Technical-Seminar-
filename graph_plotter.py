import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle
from PIL import Image

G = nx.read_gpickle('output/time_allocated_graph.gpickle')
num_cores = 0
time_max = 0
data_list = G.nodes(data='core')
for data in data_list:
    if data[1] > num_cores:
        num_cores = data[1]
data_list = G.nodes(data='end_time')
for data in data_list:
    if data[1] > time_max:
        time_max = data[1]

fig, axs = plt.subplots(num_cores + 1,1)

fig.tight_layout()

for ind, ax in enumerate(axs):
    ax.set_title(f'Core {ind}', loc='left')
    ax.set_xlim([0,time_max])
    ax.set_ylim([0,1])
    ax.set_xticks(range(0,time_max+1))
    ax.axes.get_yaxis().set_visible(False)

for node in G.nodes(data=True):
    start_time = node[1]['start_time']
    end_time = node[1]['end_time']
    task_core = node[1]['core']
    task_color = node[1]['color']
    task_width = end_time - start_time
    task_label = node[0]
    task_label = task_label.replace(',','_')
    axs[task_core].bar(x=start_time,height=0.5,width=task_width, align='edge', color=task_color, edgecolor='black')
    axs[task_core].text(x=(start_time + task_width/2), y=0.25, ha='center', va='bottom',s=task_label)

plt.savefig('output/time_allocation.png')
plt.show()
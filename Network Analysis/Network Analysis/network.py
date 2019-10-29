import ndlib
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
from ndlib.utils import multi_runs
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from networkx.generators.degree_seq import expected_degree_graph

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import networkx as nx
import json
import warnings

n = 271269  # n nodes
p = 0.007286
w = [p * n for i in range(n)]  # w = p*n for all nodes
g = expected_degree_graph(w)  # configuration model
largest_subgraph1 = max(nx.connected_component_subgraphs(g), key=len)
pos = nx.spring_layout(largest_subgraph1, k=0.05)
nx.draw(largest_subgraph1, pos=pos, cmap=plt.cm.PiYG, edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
nx.draw_networkx(largest_subgraph1, pos=pos)
plt.savefig('graphfinal2.png')
model = ep.SIRModel(largest_subgraph1)

cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.05) # infection rate
cfg.add_model_parameter('gamma', 0.05) # recovery rate
cfg.add_model_parameter("percentage_infected", 0.01)
model.set_initial_status(cfg)

iterations = model.iteration_bunch(200, node_status=True)
trends = model.build_trends(iterations)

viz = DiffusionTrend(model, trends)
viz.plot()
viz = DiffusionPrevalence(model, trends)
viz.plot()

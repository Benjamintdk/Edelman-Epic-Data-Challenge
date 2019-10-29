from igraph import *
import numpy as np
import cProfile

g = Graph.Read_GraphML("actual.xml")

# Plot the graph
plot(g, vertex_size=1, output="graph-draw-fr.png")

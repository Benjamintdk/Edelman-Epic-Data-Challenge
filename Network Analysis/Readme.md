# Run the python scripts in the following order on the tweets.json dataset. 

Preprocess the dataset:
```bash
python parseJson.py
```
Plots the actual graph and generates centrality and node values, etc:
```bash
python tweets_analysis.py
```
Plots the simulator graph:
```bash
python network.py
```
Plots final graph using Igraph library:
```bash
python print_graph_tool.py
```

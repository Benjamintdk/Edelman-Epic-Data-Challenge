#Import module

#handling data
import pandas as pd
import numpy as np
from scipy import stats
from operator import itemgetter

#handling information
import re
import json

#handling plots
import matplotlib.pyplot as plt
import seaborn as sns

#for network creation
import networkx as nx

import csv

pd.set_option('display.float_format', lambda x: '%.f' % x)

# Read json into a pandas dataframe
tweets_df = pd.read_json("data.json")
articles = pd.read_json("articles.json")
output_articles = []
# Create a second dataframe to put important information
tweets_final = pd.DataFrame(columns = ["created_at", "id", "in_reply_to_screen_name", "in_reply_to_status_id", "in_reply_to_user_id",
                                      "retweeted_id", "retweeted_screen_name", "user_mentions_screen_name", "user_mentions_id",
                                       "text", "user_id", "screen_name", "followers_count", "url"])

# Columns that are going to be the same
equal_columns = ["created_at", "id", "text"]
# tweets_final = tweets_df.filter(equal_columns, axis=1)
tweets_final[equal_columns] = tweets_df[equal_columns]

# Get the basic information about user
def get_basics(tweets_final):
	tweets_final["screen_name"] = tweets_df["user"].apply(lambda x: x["screen_name"])
	tweets_final["user_id"] = tweets_df["user"].apply(lambda x: x["id"])
	tweets_final["followers_count"] = tweets_df["user"].apply(lambda x: x["followers_count"])
	tweets_final["url"] = tweets_df['entities'].apply(lambda x: x['urls'])
	return tweets_final

# Get the user mentions
def get_usermentions(tweets_final):
    # Inside the tag 'entities' will find 'user mentions' and will get 'screen name' and 'id'
    tweets_final["user_mentions_screen_name"] = tweets_df["entities"].apply(lambda x: x["user_mentions"][0]["screen_name"] if x["user_mentions"] else np.nan)
    tweets_final["user_mentions_id"] = tweets_df["entities"].apply(lambda x: x["user_mentions"][0]["id_str"] if x["user_mentions"] else np.nan)
    return tweets_final

# Get retweets
def get_retweets(tweets_final):
	try:
		tweets_final["retweeted_screen_name"] = tweets_df["retweeted_status"].apply(lambda x: x["user"]["screen_name"] if x is not np.nan else np.nan)
		tweets_final["retweeted_id"] = tweets_df["retweeted_status"].apply(lambda x: x["user"]["id_str"] if x is not np.nan else np.nan)
	except KeyError as e:
		tweets_final['retweeted_screen_name'] = None
		tweets_final['retweeted_id'] = None
	return tweets_final

# Get the information about replies
def get_in_reply(tweets_final):
    # Just copy the 'in_reply' columns to the new dataframe
    tweets_final["in_reply_to_screen_name"] = tweets_df["in_reply_to_screen_name"]
    tweets_final["in_reply_to_status_id"] = tweets_df["in_reply_to_status_id"]
    tweets_final["in_reply_to_user_id"]= tweets_df["in_reply_to_user_id"]
    return tweets_final

# Lastly fill the new dataframe with the important information
def fill_df(tweets_final):
    get_basics(tweets_final)
    get_usermentions(tweets_final)
    get_retweets(tweets_final)
    get_in_reply(tweets_final)
    return tweets_final

# Get the interactions between the different users
def get_interactions(row):
    # From every row of the original dataframe
    # First we obtain the 'user_id' and 'screen_name'
    user = row["user_id"], row["screen_name"]
    # Be careful if there is no user id
    if user[0] is None:
        return (None, None), []

    # The interactions are going to be a set of tuples
    interactions = set()

    # Add all interactions
    # First, we add the interactions corresponding to replies adding the id and screen_name
    interactions.add((row["in_reply_to_user_id"], row["in_reply_to_screen_name"]))
    # After that, we add the interactions with retweets
    interactions.add((row["retweeted_id"], row["retweeted_screen_name"]))
    # And later, the interactions with user mentions
    interactions.add((row["user_mentions_id"], row["user_mentions_screen_name"]))

    # Discard if user id is in interactions
    interactions.discard((row["user_id"], row["screen_name"]))
    # Discard all not existing values
    interactions.discard((None, None))
    # Return user and interactions
    return user, interactions

tweets_final = fill_df(tweets_final)
tweets_final = tweets_final.where((pd.notnull(tweets_final)), None)
graph = nx.Graph()
i1 = 0

for index, tweet in tweets_final.iterrows():
    user, interactions = get_interactions(tweet)
    user_id, user_name = user
    tweet_id = tweet["id"]
    #tweet_sent = tweet["sentiment"]
    for interaction in interactions:
      int_id, int_name = interaction
      graph.add_edge(user_id, int_id, tweet_id = tweet_id)
      graph.node[user_id]["name"] = user_name
      graph.node[int_id]["name"] = int_name

print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges present in the Graph")
degrees = [val for (node, val) in graph.degree()]
print(f"The maximum degree of the Graph is {np.max(degrees)}")
print(f"The minimum degree of the Graph is {np.min(degrees)}")
print(f"The average degree of the nodes in the Graph is {np.mean(degrees):.1f}")
print(f"The most frequent degree of the nodes found in the Graph is {stats.mode(degrees)[0][0]}")

### CODE TO FIND LEAST PROPAGATED ARTICLES AGAINST TWEETS
largest_subgraph = max(nx.connected_component_subgraphs(graph), key=len)
nx.write_graphml(max_subgraphs, "max.xml")

graphs.remove(max(graphs, key=len))
for graph in graphs:
	texts = tweets_final.loc[tweets_final['user_id'] == nx.center(graph)[0]]['url']
	textsL = texts.tolist()
	if len(textsL) > 0:
		for text in textsL:
			try:
				row = articles.loc[articles['link'] == text[0]['expanded_url']]
				if not row.empty:
					output_articles.append(text[0]['expanded_url'])
			except Exception as e:
				continue
#print(pd.DataFrame(output_articles).columns.values.tolist())
pd.DataFrame(output_articles).to_csv('out.csv', index=False)

	print(f"There are {largest_subgraph.number_of_nodes()} nodes and {largest_subgraph.number_of_edges()} \
edges present in the largest component of the Graph")
if nx.is_connected(graph):
    print("The graph is connected")
else:
    print("The graph is not connected")
print(f"The average clustering coefficient is {nx.average_clustering(largest_subgraph)} in the largest subgraph")
print(f"The transitivity of the largest subgraph is {nx.transitivity(largest_subgraph)}")
print(f"The diameter of our Graph is {nx.diameter(largest_subgraph)}")
print(f"The average distance between any two nodes is {nx.average_shortest_path_length(largest_subgraph):.2f}")

graph_centrality = nx.degree_centrality(largest_subgraph)
max_de = max(graph_centrality.items(), key=itemgetter(1))
graph_closeness = nx.closeness_centrality(largest_subgraph)
max_clo = max(graph_closeness.items(), key=itemgetter(1))
graph_betweenness = nx.betweenness_centrality(largest_subgraph, normalized=True, endpoints=False)
max_bet = max(graph_betweenness.items(), key=itemgetter(1))
print(f"the node with id {max_de[0]} has a degree centrality of {max_de[1]:.2f} which is the maximum of the Graph")
print(f"the node with id {max_clo[0]} has a closeness centrality of {max_clo[1]:.2f} which is the maximum of the Graph")
print(f"the node with id {max_bet[0]} has a betweenness centrality of {max_bet[1]:.2f} which is the maximum of the Graph")

node_and_degree = largest_subgraph.degree()
colors_central_nodes = ['orange', 'red']
pos = nx.spring_layout(largest_subgraph, k=0.05)
plt.figure(figsize = (10, 10))
nx.draw(largest_subgraph, pos=pos, cmap=plt.cm.PiYG, edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(largest_subgraph, pos=pos, node_size=300)
plt.savefig('graphfinal.png')
plt.show()

import sys
import networkx
import igraph
sys.path.insert(0,"convert")
import majority_vote
import cut_graph
from convert_graphtypes import *

g=g_load("Darren.gpickle")

l=cut_graph.comm_fast_greed(g)


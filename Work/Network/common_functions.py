import networkx
import igraph

def clustering_coff(G,weight=None):
    if isinstance(G,networkx.Graph):
        return networkx.clustering(G,weight=weight)
    elif isinstance(G,igraph.Graph):
        return G.transivity_local_undirected() #Note, don't know if this is what is expected

def k_nearest_neighbours(G,weight=None):
    if isinstance(G,networkx.Graph):
        return networkx.k_nearest_neighbours()
    elif isinstance(G,igraph.Graph):
        return G.transitivity_undirected()


    

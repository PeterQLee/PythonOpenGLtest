import networkx
import majority_vote
import igraph
import sys
import operator
import cairo
sys.path.insert(0,"./convert")

from convert_graphtypes import *
from cut_graph import *
ng=g_load("Darren.gpickle")
ig=networkx_to_igraph(ng)

# a=ig.community_leading_eigenvector().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_leading_eigenvector()
# # plot_graph(l,'G_cut.community_leading_eigenvector.png')
# a=ig.community_fastgreedy().as_clustering().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_fastgreedy().as_clustering()
# plot_graph(l,'G_cut.community_fastgreedy.png')

# a=ig.community_infomap().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_infomap()
# plot_graph(l,'G_cut.community_infomap.png')

# a=ig.community_label_propagation().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_label_propagation()
# plot_graph(l,'G_cut.community_label_propagation.png')

# a=ig.community_multilevel().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_multilevel()
# plot_graph(l,'G_cut.community_multilevel.png')

# a=ig.community_spinglass().subgraph(0)

# G=delete_common_nodes(ig,a)
# l=ig.community_spinglass()
# plot_graph(l,'G_cut.community_spinglass.png')

a=ig.community_walktrap().as_clustering().subgraph(0)

G=delete_common_nodes(ig,a)
l=ig.community_walktrap().as_clustering()
plot_graph(l,'G_cut.community_walktrap.png')


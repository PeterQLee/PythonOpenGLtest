import networkx
import majority_vote
import igraph
import sys
import operator
import cairo
import traceback
sys.path.insert(0,"./convert")

from convert_graphtypes import *
def snip_snip(G):
    netgraph=G
    #if isinstance(G) == networkx.Graph:
    #    netgraph=convert_graphtypes.networkx_to_igraph(G)

def clique(gr):
    G=g_load(gr)
    li=list(list(networkx.k_clique_communities(G,2))[0])
    
    mv=majority_vote.list_majority(li,G)
    #print(mv)
    #s=sorted(mv.items(),key=operator.itemgetter(1),reverse=True)
    return mv


def k_best_attr(gr,attr,k):
    #gets the nodes with the best attributes
    G=g_load(gr)
    order_li=[]

    for i in range(len(G)):
        order_li.append(G.nodes()[i])
        
    return sorted(order_li,key=lambda x:G.node[x][attr],reverse=True)[:k]

def community_fastgreedy(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_fastgreedy().as_clustering()

def community_infomap(gr,trials=10):
    #G=networkx_to_igraph(g_load(gr),trials=trials)
    return gr.community_infomap()

def community_eigenvector_naive(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_leading_eigenvector_naive()

def community_leading_eigenvector(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_leading_eigenvector()

def community_label_propagation(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_label_propagation()

def community_multilevel(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_multilevel()

def community_optimal_modularity(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_optimal_modularity()

def community_edge_between(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_leading_eigenvector_naive()

def community_spinglass(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_spinglass()

def community_walktrap(gr):
    #G=networkx_to_igraph(g_load(gr))
    return gr.community_walktrap().as_clustering()

def plot_graph(l,fout):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    #o=igraph.plot(l.as_clustering(),target=s,layout="fr",vertex_label=[i["name"] for i in l.as_clustering().graph.vs])
    o=igraph.plot(l,target=s,layout="fr",vertex_label=[i["name"] for i in l.graph.vs])
    o.save(fout)

def cut_community():
    #cuts the least connected community
    pass


def plot_all(gr):
    G=networkx_to_igraph(g_load(gr))
    #[G.community_fastgreedy,G.community_infomap,G.community_leading_eigenvector_naive,G.community_leading_eigenvector,G.community_label_propagation,G.community_multilevel,G.community_optimal_modularity,G.community_spinglass,G.community_walktrap]
    #
    funclist=[G.community_fastgreedy,G.community_infomap,G.community_leading_eigenvector,G.community_label_propagation,G.community_multilevel,G.community_spinglass,G.community_walktrap]
    #name_list=['G.community_fastgreedy','G.community_infomap','G.community_leading_eigenvector_naive','G.community_leading_eigenvector','G.community_label_propagation','G.community_multilevel','G.community_optimal_modularity','G.community_spinglass','G.community_walktrap']
    name_list=['G.community_fastgreedy','G.community_infomap','G.community_leading_eigenvector','G.community_label_propagation','G.community_multilevel','G.community_spinglass','G.community_walktrap']
    n_dict={}
    
    for i in range(len(funclist)):
        f=funclist[i]()
        if isinstance(f,igraph.VertexDendrogram):
            f=f.as_clustering()
        
        plot_graph(f,name_list[i]+".png")
        n_dict[name_list[i]]=list(f)

        
    return n_dict

def plot_cut(gr):
    G=networkx_to_igraph(g_load(gr))
    

    name_list=['G_cut.community_fastgreedy','G_cut.community_infomap','G_cut.community_leading_eigenvector','G_cut.community_label_propagation','G_cut.community_multilevel','G_cut.community_spinglass','G_cut.community_walktrap']
    n_dict={}
    funclist=[community_fastgreedy,community_infomap,community_leading_eigenvector,community_label_propagation,community_multilevel,community_spinglass,community_walktrap]    
    for i in range(len(funclist)):
        try:            
           
            G=networkx_to_igraph(g_load(gr))

            f=funclist[i](G)
            if isinstance(f,igraph.VertexDendrogram):
                f=f.as_clustering()
            
            leastind=-1
            leastval=1
            kk=f.subgraphs()

            for Q in range(len(kk)):
                p=kk[Q].transitivity_undirected()
                if p<leastval:
                    leastval=p
                    leastind=Q
                    
            try:
                delete_common_nodes(G,f.subgraph(leastind))
            except:
                traceback.print_exc()
            f=funclist[i](G)

            if isinstance(f,igraph.VertexDendrogram):
                f=f.as_clustering()

            plot_graph(f,name_list[i]+".png")

            n_dict[name_list[i]]=list(f)
        except:

            traceback.print_exc()
        
    return n_dict
    
def cut_lowest_subgraph(G,F):
    cluster=F(G)
    s_G=cluster.subgraphs()
    leastval=99
    leastind=-1
    for Q in range(len(s_G)):
        p=s_G[Q].transitivity_undirected()
        if p<leastval:
            leastval=p
            leastind=Q
    if leastind==-1: return
    delete_common_nodes(G,cluster.subgraph(leastind))

def delete_common_nodes(G1,G2,attr="id"):
    j=len(G1.vs)-1
    for i in range(len(G2.vs)-1,-1,-1):

        while G1.vs[j].attributes()[attr]!=G2.vs[i].attributes()[attr]:
            j-=1
        if G1.vs[j].attributes()['screen_name']!=u'dwmacleod':
            G1.delete_vertices(j)
            G2.delete_vertices(i)
            
        j-=1
    
        

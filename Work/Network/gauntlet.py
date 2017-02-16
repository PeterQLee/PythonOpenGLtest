##Essentially makes everygraph run the community structure gauntlet
import cut_graph
import networkx
import majority_vote 
import sys
import os
import traceback
sys.path.insert(0,"convert")
from convert_graphtypes import *


def DO_community(G,F,rightloc,rank_list):
    iG=networkx_to_igraph(G)
    p_edge=-1
    p_vert=-1
    c=0
    while p_edge!=len(iG.vs) and p_vert!=len(iG.es) and c<=3:
        cut_graph.cut_lowest_subgraph(iG,F)
        #print(p_edge,p_vert,len(iG.es),len(iG.vs))
        p_edge=len(iG.es)
        p_vert=len(iG.vs)
        c+=1
        
    f_g=F(iG).subgraphs()
    #find top five for each subgraph
    del iG
    c=0
    highest_loc=None
    highest_trans=0
    for i in f_g:
        trans=i.transitivity_undirected()
        X=igraph_to_networkx(i)
        t=majority_vote.niave_majority(X,poi)
        locs_=majority_vote.rank(t,5)
        if trans> highest_trans:
            highest_trans=trans
            highest_loc=locs_
        print("Subgraph %s, trans:%s, with locations %s"%(str(c),str(trans),str(locs_)))
        del X
        c+=1

    #update the frequency count for the location of highest occurance
    for i in range(len(highest_loc)):
        if highest_loc[i][0]==rightloc:

            for j in range(i,len(rank_list)):
                rank_list[j]+=1
    
            break
    
    del f_g




if __name__=='__main__':
    indir='graphs/'
    outdir='testgraphs/'
    
    graph_funcs=[cut_graph.community_fastgreedy,cut_graph.community_infomap,cut_graph.community_leading_eigenvector,cut_graph.community_label_propagation,cut_graph.community_multilevel,cut_graph.community_spinglass,cut_graph.community_walktrap]

    name_list=["\nFast greedy:","\nInfomap:","\nLeading eigenvector:","\nLabel Propagation:","\nMultilevel:","\nSpinglass:","\nWalktrap:"]

    using=0

    

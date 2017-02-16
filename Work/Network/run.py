import cut_graph
import networkx
import majority_vote 
import sys
import os
import traceback
sys.path.insert(0,"convert")
from convert_graphtypes import *

def find_poi(st):
    '''finds poi given the file name'''
    #EX: 
    #USA_150705043_21_78.gpickle
    li=st.split("_")
    return int(li[1])
def find_actual_loc(g,poi):
    return g.node[poi]

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
    top=[0,0,0,0,0]
    total=0

    graph_funcs=[cut_graph.community_fastgreedy,cut_graph.community_infomap,cut_graph.community_leading_eigenvector,cut_graph.community_label_propagation,cut_graph.community_multilevel,cut_graph.community_spinglass,cut_graph.community_walktrap]

    name_list=["\nFast greedy:","\nInfomap:","\nLeading eigenvector:","\nLabel Propagation:","\nMultilevel:","\nSpinglass:","\nWalktrap:"]
    
    rank_list=[]
    for i in range(len(graph_funcs)):
        rank_list.append([0,0,0,0,0])

    rank_totals=[0]*len(graph_funcs)
    
    dir=os.listdir('graphs_all')
    
    for p in dir:
        print(p)
        #iterate through each graph in directory
        poi=find_poi(p)
        G=networkx.read_gpickle('graphs_all/'+p)
        
        actual_loc=find_actual_loc(G,poi)
        #print ("____________________")
        #print("Person %s\nActual location is %s"%(str(poi),actual_loc))
    

        ####################
        #Uncomment for regular majority vote
        #t=majority_vote.niave_majority(G,poi)
        #locs_niave=majority_vote.rank(t,5)

        ##################
        #Uncomment for  city and state (no blanks allowed)
        #test_maj=majority_vote.rank(majority_vote.test_majority(G,poi),5)

        #############
        #Uncomment for country wide majority
        #t=majority_vote.country_majority(G,poi)
        ###locs_country=majority_vote.rank(t,5)

        #print ("Top five majority locations are %s"%str(test_maj))

        for i in range(len(locs_country)):

            ######################################
            #Uncomment for city and state (no blanks allowed)
            #if test_maj[i][0]==(majority_vote.anglisize(actual_loc["city"]).lower(),majority_vote.anglisize(actual_loc["state"]).lower()):
            ######################################
            #Uncomment for only state
            #if locs_niave[i][0]==("",majority_vote.anglisize(actual_loc["state"].lower())):
            ##############################
            #Uncomment for country
            #print locs_country[i], actual_loc['country']
            topbefore=top[0]
            if locs_country[i][0]==majority_vote.anglisize(actual_loc["country"]).lower():
                for j in range(i,len(top)):
                    top[j]+=1
                break
            if top[0]==topbefore:
                print G.node
        total+=1

        #try doing the clique divisions
        #clique_loc=cut_graph.clique(G)
        #print ("Top five clique locations are %s"%str(majority_vote.rank(clique_loc,5)))
            

        #Do fast_greedy communities
        '''
        for i in range(len(graph_funcs)):
            print(name_list[i])
            try:
                DO_community(G,graph_funcs[i],(actual_loc['city'],actual_loc['state']),rank_list[i])
                rank_totals[i]+=1
            except:
                traceback.print_exc()
        '''

    #print final ranking results for majority
    print([float(i)/float(total) for i in top])


    #print final results for community
    '''
    for i in range(len(rank_list)):
        print (name_list[i],[float(j)/float(rank_totals[i]) for j in rank_list[i]]) 
1'''

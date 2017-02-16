import cut_graph
import numpy
import networkx
import majority_vote 
import sys
import os
import traceback
sys.path.insert(0,"convert/")
sys.path.insert(0,"distance/")
from convert_graphtypes import *
from haversine import HaversineDistance
from run import find_poi
import copy

def norm(s):
    return majority_vote.anglisize(s).lower()

def distance_group(t):
    #grouops similar coordinates as same location
    has=[]
    coords=[]
    count=[]


    for i in t:
        #group closest ones to poi as same group
        #if i==newkey:continue
        
        if (norm(i[0]),norm(i[1])) in has:
            x=has.index((norm(i[0]),norm(i[1])))
        else:
            x=-1
        #group similarly listed ones
        if x!=-1:
            coords[x]=(float(i[2]*t[i]+coords[x][0]*count[x])/float(t[i]+count[x]),
                    float(i[3]*t[i]+coords[x][1]*count[x])/float(t[i]+count[x]))
            count[x]+=t[i]
            #todelete
        
        else:
            has.append((norm(i[0]),norm(i[1])))
            coords.append((i[2],i[3]))
            count.append(t[i])
    ret={}
    for i in range(len(has)):
        ret[has[i]+coords[i]]=count[i]
            
    return ret
    
       
def distance_community(G,F,pkey, rank_list): #BROKEN
    iG=networkx_to_igraph(G)

    #cut lowest transitivity graph
    cut_graph.cut_lowest_subgraph(iG,F)

        
    f_g=F(iG).subgraphs()
    #find top five for each subgraph
    del iG
    c=0
    highest_loc=None
    highest_trans=0
    for i in f_g:
        trans=i.transitivity_undirected()
        X=igraph_to_networkx(i)
        t=majority_vote.coord_majority(X,poi)
        distance_group(t,pkey,None,100)
        locs_=majority_vote.rank(t,5)
        if trans> highest_trans:
            highest_trans=trans
            highest_loc=locs_
        #print("Subgraph %s, trans:%s, with locations %s"%(str(c),str(trans),str(locs_)))
        del X
        c+=1

    #update the frequency count for the location of highest occurance
    if highest_loc:
        for i in range(len(highest_loc)):
            if highest_loc[i][0]==pkey:

                for j in range(i,len(rank_list)):
                    rank_list[j]+=1
    
                break
    
    del f_g



if __name__=='__main__':
    jaccard=0
    perc_conn=1

    weight_fields=["jaccard","perc_conn"]
    
    
    top=[0,0,0,0,0]
    total=0
    graph_funcs=[cut_graph.community_fastgreedy,cut_graph.community_infomap,cut_graph.community_leading_eigenvector,cut_graph.community_label_propagation,cut_graph.community_multilevel,cut_graph.community_spinglass,cut_graph.community_walktrap]
    name_list=["\nFast greedy:","\nInfomap:","\nLeading eigenvector:","\nLabel Propagation:","\nMultilevel:","\nSpinglass:","\nWalktrap:"]
    threshold=10
    dir=os.listdir('graphs_all/')
    badcount=0
    all_deltas=[]
    
    rank_list=[]

    
    weight_type=jaccard
    
    for i in range(len(graph_funcs)):
        rank_list.append([0,0,0,0,0])
    rank_totals=[0]*len(graph_funcs)
    
    for p in dir:
        print p
        poi=find_poi(p)
        retrieve=(('city',),('state',),('coordinates','lng'),('coordinates','lat'))
        G=networkx.read_gpickle('graphs_all/'+p)
        person=G.node[poi]
        poi_coord=person['coordinates']
        t=majority_vote.majority(G,poi,retrieve)
        if 'lng' not in poi_coord:
            continue
        newkey=(norm(person['city']),norm(person['state']),poi_coord['lng'],poi_coord['lat'])

        
        ############
        #DEBUG Code
        # if newkey not in t:
        #      for i in t:
        #          if (i[0],i[1])==(newkey[0],newkey[1]):
        #              for j in G.node:
        #                  if 'lng' not in  G.node[j]['coordinates']: continue

        #                  if i[2]==G.node[j]["coordinates"]["lng"] and i[3]==G.node[j]["coordinates"]["lat"]:
        #                      print person["location"],G.node[j]["location"]

        #group according to distance
        
        T=distance_group(t)
        
        loco=majority_vote.rank(T,5)

        for i in range(len(loco)):
            #add score to appopriate categories
            #print loco[i], newkey
            
            delta= HaversineDistance(newkey[2],newkey[3],loco[i][0][2],loco[i][0][3])
            if delta[0]<=threshold:

                for j in range(i,len(top)):
                    top[j]+=1
                break

        total+=1
        
        #################
        #Start community structures
        
        # for i in range(len(graph_funcs)):
        
        #     try:
        #         distance_community(G,graph_funcs[i],newkey,rank_list[i])
        #         rank_totals[i]+=1
        #     except:
        #         traceback.print_exc()

    
    print([float(i)/float(total) for i in top])
    
    # print all_deltas
    # try:
    #     print "Mean ", numpy.mean(all_deltas)
    #     print "Median ", numpy.median(all_deltas)
    #     print "Standard dev. ", numpy.std(all_deltas)
    # except:
    #     print "ERRO! ",all_deltas

    # for i in range(len(rank_list)):
    #     print (name_list[i],[float(j)/float(rank_totals[i]) for j in rank_list[i]]) 

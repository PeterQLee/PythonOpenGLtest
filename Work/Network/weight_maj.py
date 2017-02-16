import cut_graph
import numpy
import networkx
import majority_vote
import numpy
import sys
import os
import traceback
sys.path.insert(0,"convert/")
sys.path.insert(0,"distance/")
from convert_graphtypes import *
from haversine import HaversineDistance
from run import find_poi
import copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def calc_score(G,loc,poi):
    #calculates the given average score of the people following
    score=0
    num=0

    for i in G.nodes():
        if i==poi:continue
        if majority_vote.anglisize(G.node[i]['city']).lower()==majority_vote.anglisize(loc[0]).lower() and majority_vote.anglisize(G.node[i]['state']).lower()==majority_vote.anglisize(loc[1]).lower():
            score+=calc_metric(G.node[i])
            num+=1
    if num==0:return 1j
    return score/float(num)
    
def calc_metric(N):
    return float(N['connectivity'])
def distance_group(t):
    #grouops similar coordinates as same location
    has=[]
    coords=[]
    count=[]


    for i in t:
        #group closest ones to poi as same group
        if i==newkey:continue

        if (i[0],i[1]) in has:
            x=has.index((i[0],i[1]))
        else:x=-1
        #group similarly listed ones
        if x!=-1:
            coords[x]=(float(i[2]*t[i]+coords[x][0]*count[x])/float(t[i]+count[x]),
                    float(i[3]*t[i]+coords[x][1]*count[x])/float(t[i]+count[x]))
            count[x]+=t[i]
            #todelete
        
        else:
            has.append((majority_vote.anglisize(i[0]).lower(),majority_vote.anglisize(i[1]).lower()))
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

def assemble_weight_list(G,poi,field):
    #get the associated weights
    li=[]
    for i in G.node:

        #li.append(1)
        T=G.node[i]
        val=1
        if T['followers']!=0:
            val*=T['followers']**(-0.05)
        else:
            val=0
        if T['followed']!=0:
            val*=T['followed']**(-0.2)
        else:
            val=0
        if T['connectivity']!=0:
            val*=T['connectivity']**(-0.15)

            
        if T['jaccard_coef']!=0:
            val*=T['jaccard_coef']**(0)

        li.append(val)
    
    return li








if __name__=='__main__':
    jaccard=0
    perc_conn=1
    connectivity=2
    weight_fields=["jaccard_coef","perc_connectivity",'connectivity']
        
    score_l=[]
    score_y=[]
    
    top=[0,0,0,0,0]
    total=0
    graph_funcs=[cut_graph.community_fastgreedy,cut_graph.community_infomap,cut_graph.community_leading_eigenvector,cut_graph.community_label_propagation,cut_graph.community_multilevel,cut_graph.community_spinglass,cut_graph.community_walktrap]
    name_list=["\nFast greedy:","\nInfomap:","\nLeading eigenvector:","\nLabel Propagation:","\nMultilevel:","\nSpinglass:","\nWalktrap:"]
    threshold=10
    DNAME='graphs/'
    
    dir=os.listdir(DNAME)
    badcount=0
    all_deltas=[]
    
    rank_list=[]

    exact_q=(('city',),('state',))
    coord_q=(('city',),('state',),('coordinates','lng'),('coordinates','lat'))
    
    weight_type=connectivity
    
    for i in range(len(graph_funcs)):
        rank_list.append([0,0,0,0,0])
    rank_totals=[0]*len(graph_funcs)
    
    for p in dir:
        #print p
        poi=find_poi(p)
        retrieve=exact_q
        G=networkx.read_gpickle(DNAME+p)
        person=G.node[poi]
        #print (person)
        poi_coord=person['coordinates']
        weightlist=assemble_weight_list(G,poi,None)#weight_fields[weight_type])

        
        t=majority_vote.majority(G,poi,retrieve,weights=weightlist)#weightlist)
        if 'lng' not in poi_coord:
            continue
#        newkey=(majority_vote.anglisize(person['city'].lower()),majority_vote.anglisize(person['state'].lower()),poi_coord['lng'],poi_coord['lat'])
        newkey=(majority_vote.anglisize(person['city'].lower()),majority_vote.anglisize(person['state'].lower()))

        
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
        
        #T=distance_group(t)
        ################
        T=t
        #print (T)
        loco=majority_vote.rank(T,len(T))
        ch=False
        F=0
        for i in range(len(loco)):
            #add score to appopriate categories

            F=i
            #delta= HaversineDistance(newkey[2],newkey[3],loco[i][0][2],loco[i][0][3])
            #if delta[0]<=threshold:
            
            if newkey==(majority_vote.anglisize(loco[i][0][0]).lower(),majority_vote.anglisize(loco[i][0][1]).lower()):
                #if (newkey[0],newkey[1])==(majority_vote.anglisize(loco[i][0][0]).lower(),majority_vote.anglisize(loco[i][0][1]).lower()):
                    for j in range(i,len(top)):
                        top[j]+=1
        #                if j==0:
        #                    ch=True
        
                    break
        poi_info=newkey
        conn_info=(loco[0][0][0],loco[0][0][1])
       
        conn_score=calc_score(G,conn_info,poi)
        ground_score=calc_score(G,poi_info,poi)
        
       

        #A positive score indicates that the ground truth has a higher connectivity per follower of follower
        #than the majority vote

        if ground_score!=1j and ground_score!=conn_score:
            score_y.append(ground_score-conn_score)
            score_l.append(len(G))
#            score_l.append(conn_score)

        #if not conn_score
            #TODO, DELETE
            # for m in loco:
        
            #     if newkey==(majority_vote.anglisize(m[0][0]).lower(),majority_vote.anglisize(m[0][1]).lower()):
                    
            #         print m,loco[0], len(G)
                    
                    
            #         for i in G.nodes():
            #             if majority_vote.anglisize(G.node[i]['city']).lower()==majority_vote.anglisize(m[0][0]).lower() and majority_vote.anglisize(G.node[i]['state']).lower()==majority_vote.anglisize(m[0][1]).lower():
                            
            #                 print G.node[i]
            #                 conn_score+=calc_metric(G.node[i])
            #                 conn_num+=1
            #         print "_______________________\n\n\n"
            
        total+=1
        
        #################
        #Start community structures
        
        # for i in range(len(graph_funcs)):
        
        #     try:
        #         distance_community(G,graph_funcs[i],newkey,rank_list[i])
        #         rank_totals[i]+=1
        #     except:
        #         traceback.print_exc()

    print (top)
    print([float(i)/float(total) for i in top])

    print ( numpy.mean(numpy.array(score_y)-numpy.array(score_l)))
    
    plt.scatter(score_l,score_y)
    plt.xlabel('network size')
    plt.ylabel('ground - maj  score')
    plt.savefig('maj_vs_ground_scores.png')
    # print all_deltas
    # try:
    #     print "Mean ", numpy.mean(all_deltas)
    #     print "Median ", numpy.median(all_deltas)
    #     print "Standard dev. ", numpy.std(all_deltas)
    # except:
    #     print "ERRO! ",all_deltas

    # for i in range(len(rank_list)):
    #     print (name_list[i],[float(j)/float(rank_totals[i]) for j in rank_list[i]]) 

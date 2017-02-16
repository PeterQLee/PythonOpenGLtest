import networkx
import sys
import os
sys.path.insert(0,"../")
sys.path.insert(0,"../convert/")
import run
import cut_graph
from datetime import datetime
import numpy

import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from convert_graphtypes import *

def diff_create(p1,p2):
    #gets the difference of two accounts, in seconds
    pattern='%a %d %b %Y %I:%M:%S %p '
    pattern2='%d/%m/%Y %I:%M:%S %p'
    try:
        date_1 = datetime.strptime(p1, pattern)
        #note, may need to use absolute function here later
    except:
        date_1 = datetime.strptime(p1, pattern2)

    try:
        date_2 = datetime.strptime(p2, pattern)
    except:
        date_2 = datetime.strptime(p2, pattern2)
        
    return (date_1-date_2).total_seconds()/60/60/24

def DO_COMM_nocut(G,F):
    #gets highest community, without any cuts
    iG=networkx_to_igraph(G)
    f_g=F(iG).subgraphs()
    high_trans=0
    high_graph=None
    for i in f_g:
        trans=i.transitivity_undirected()
        if trans> high_trans:
            high_trans=trans
            high_graph=i

    if high_graph:
        return igraph_to_networkx(high_graph)
    return None

DIRP='../graphs/'
if __name__=='__main__':
    graph_funcs=[cut_graph.community_fastgreedy,cut_graph.community_infomap,cut_graph.community_leading_eigenvector,cut_graph.community_label_propagation,cut_graph.community_multilevel,cut_graph.community_spinglass,cut_graph.community_walktrap]

    name_list=["\nFast greedy:","\nInfomap:","\nLeading eigenvector:","\nLabel Propagation:","\nMultilevel:","\nSpinglass:","\nWalktrap:"]
    comm_diffs={}
    for i in name_list:
        comm_diffs[i]=[]
    print 'mean', 'std'
    dir=os.listdir(DIRP)
    allgraphs=[]
    allpoi=[]

    persstats=[]
    poststats=[]
    for p in dir:
        poi=run.find_poi(p)
        
        G=networkx.read_gpickle(DIRP+p)
        allgraphs.append(G)
        allpoi.append(poi)
        date=G.node[poi]["created_at"]
        diffs=[]
        for j in G.nodes():
            if j==poi:
                continue
            date2=G.node[j]["created_at"]
            diffs.append(diff_create(date,date2))
            
        npdiffs=numpy.array(diffs)

        print numpy.mean(npdiffs),numpy.std(npdiffs), numpy.median(npdiffs)
        persstats.append((numpy.mean(npdiffs),numpy.std(npdiffs),numpy.median(npdiffs)))


        #try community structures
        for g in range(len(graph_funcs)):
            F=DO_COMM_nocut(G,graph_funcs[g])
            diffS=[]
            if F:
                for j in F.nodes():
                    if j==poi:continue
                    date2=F.node[j]['created_at']
                    diffS.append(diff_create(date,date2))
                npdiffS=numpy.array(diffS)
                print name_list[g], numpy.mean(npdiffS), numpy.std(npdiffS)
                comm_diffs[name_list[g]].append(numpy.mean(npdiffS))


    for c in range(len(allpoi)):
        date=allgraphs[c].node[allpoi[c]]['created_at']
        diffs=[]
        for d in range(len(allgraphs)):
            if d == c: continue
            for j in allgraphs[d].nodes():
                date2=allgraphs[d].node[j]['created_at']
                diffs.append(diff_create(date,date2))

        npdiffs=numpy.array(diffs)
        poststats.append((numpy.mean(npdiffs),numpy.std(npdiffs),numpy.median(npdiffs)))

        

    avg_abs=[]
    for i in range(len(poststats)):
        print allpoi[i]," : ",poststats[i]
        print allpoi[i]," : ",persstats[i]

        avg_abs.append(abs(persstats[i][0])-abs(poststats[i][0]))

    print stats.kendalltau(persstats,poststats)
    print (numpy.mean(avg_abs))
    plt.plot(numpy.array(avg_abs),'co')
    plt.axis([0,len(avg_abs),min(avg_abs),max(avg_abs)])
    plt.grid(True)
    plt.savefig('avgs.png')
    for i in range(len(name_list)):
        print (name_list[i][1:])
        plt.clf()
        plt.plot(numpy.array(comm_diffs[name_list[i]]),'co')
        plt.axis([0,len(comm_diffs[name_list[i]]),min(comm_diffs[name_list[i]]),max(comm_diffs[name_list[i]])])
        plt.grid(True)
        plt.savefig(name_list[i][1:]+'.png')
    


    

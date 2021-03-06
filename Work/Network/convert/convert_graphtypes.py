import networkx
import igraph
#import sys

def g_load(m):
    if isinstance(m,str):
        G=networkx.read_gpickle(m)
    else:
        G=m
    return G
    

def networkx_to_igraph(netx):
    '''returns an igraph instance,given all edges, vertices, and appropriate attributes'''
    if isinstance(netx,str):
        G1=networkx.read_gpickle(netx)
    else:
        G1=netx
    id_to_int={}

    list_to_change=[]
    count=0
    
    iG=igraph.Graph(G1.order())

    for i in G1.nodes():
        #get the dictionary of each 

        id_to_int[i]=count

        for j in G1.node[i]:
            #copy each of the attributes of j into igraph

            iG.vs[count][j]=G1.node[i][j]
        iG.vs[count]["id"]=i
        count+=1
    for i in G1.edges():
        #copy each of the edges to the igraph
        #print(i)
        m=id_to_int[i[0]]
        n=id_to_int[i[1]]
        iG.add_edge(m,n,**G1.edge[i[0]][i[1]]) #unpack dict into keywords
    return iG

def igraph_to_networkx(netx):
    '''returns an igraph instance,given all edges, vertices, and appropriate attributes'''
    if isinstance(netx,str):
        iG=igraph.load(netx)
    else:
        iG=netx
    netG=networkx.Graph()
    int_to_id={}

    for i in range(len(iG.vs)):
        attr=iG.vs[i].attributes()
        int_to_id[i]=attr["id"]

        netG.add_node(attr["id"],attr_dict=attr)
        del attr["id"]
    #print(int_to_id)
    for i in range(len(iG.es)):
        m=int_to_id[iG.es[i].source]
        n=int_to_id[iG.es[i].target]
        netG.add_edge(m,n,iG.es[i].attributes())
    
    return netG

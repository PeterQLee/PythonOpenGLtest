import networkx
import numpy
import sys
import os
sys.path.insert(0,'../')
import majority_vote
from plotloc import load_py2_graph

def norm(s):
    return majority_vote.anglisize(s).lower()

def find_poi(st):
    '''finds poi given the file name'''
    #EX: 
    #USA_150705043_21_78.gpickle
    li=st.split("_")
    return int(li[1])

def normalize(data,A):
    for i in range(len(data)):
        for j in range(len(data[i][0])):
            data[i][0][j][0]/=A


def v_gf(G,poi,type='MV'):
    SIZE=2
    MAXSIZE=0
    MAXSCORE=0
    if type=='MV':
        
        D={}
            
        Vs=[]
        errormat=[]
        ground=(norm(G.node[poi]['city']),norm(G.node[poi]['state']))
        wasfound=False#TMP
        
        for i in G.node:
            if i==poi:continue
            er=0.
            loc=(norm(G.node[i]['city']),norm(G.node[i]['state']))
            if loc==ground:
                er=1.
                wasfound=True #TMP
            if loc in D:
                v=Vs[D[loc]]
                #errormat.append(er)
            else:
                D[loc]=len(Vs)
                Vs.append([0])
                v=Vs[-1]
                errormat.append([er])

            #a=G.node[i]['followed']
            b=G.node[i]['followers']

            
            #c=G.node[i]['connectivity']
            #d=G.node[i]['jaccard_ceof']
            #e=len(G)-1
            #partial=[a,b,c,d,e]

            #for i in len(range(partial)):
            #    v[i].append(partial[i])
            
            v[0]+=1
            if (v[0]>MAXSCORE): MAXSCORE=v[0]
            #if (v[1]>MAXSIZE): MAXSIZE=v[1]
        #for i in range(len(Vs)):
            #Vs[i][0]=float(Vs[i][0])/float(Vs[i][1]) #take mean


        for i in range(len(Vs)):
            Vs[i][0]/=MAXSCORE
            #ret.append((Vs[i],errormat[i]))
        return (numpy.array(Vs),numpy.array(errormat),wasfound)


    
    return None
def next_batch(size):
    random.shuffle(data)

def flatten(data):
    ret=[numpy.array(0),numpy.array(0)]
    for i in data:
        ret[0]=numpy.append(ret[0],i[0])
        ret[1]=numpy.append(ret[1],i[1])
    return ret

def vectorize_graph(dirname):
    data=[]
    MAXSCORE=0
    MAXSIZE=0
    for p in os.listdir(dirname):
        poi=find_poi(p)
        G=load_py2_graph(dirname+'/'+p)
        res=v_gf(G,poi)

        #if res[3]>MAXSIZE:
        #    MAXSIZE=res[3]
        if res[2]: #TMP
            data.append(res[:2])
        #data+=res[:2]
        #data[0]=numpy.append(data[0],res[0])
        #data[1]=numpy.append(data[1],res[1])
    #normalize(data,MAXSCORE)
    
    return data
        

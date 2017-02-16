import networkx
import numpy
import sys
import os
sys.path.insert(0,'../')
import majority_vote
from plotloc import load_py2_graph
from datetime import datetime

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

def diff_create(p1,p2):
    #gets the difference of two accounts, in seconds
    pattern='%a %d %b %Y %I:%M:%S %p '
    pattern2='%d/%m/%Y %I:%M:%S %p'
    try:
        date_1 = datetime.strptime(p1.decode('utf-8'), pattern)
        #note, may need to use absolute function here later
    except:
        date_1 = datetime.strptime(p1.decode('utf-8'), pattern2)

    try:
        date_2 = datetime.strptime(p2.decode('utf-8'), pattern)
    except:
        date_2 = datetime.strptime(p2.decode('utf-8'), pattern2)
        
    return (date_1-date_2).total_seconds()/60/60/24


def v_gf(G,poi,type='MV'):

    N_PAR=5
    MAXES=[0]*N_PAR
    if type=='MV':
        D={}
            
        Vs=[]
        errormat=[]

        date=G.node[poi]['created_at']
        ground=(norm(G.node[poi]['city']),norm(G.node[poi]['state']))
        wasfound=False#TMP
        
        for i in G.node:
            if i==poi:continue
            er=0.
            loc=(norm(G.node[i]['city']),norm(G.node[i]['state']))
            if loc[0]=='' or loc[1]=='':
                continue
            if loc==ground:
                er=1.
                wasfound=True #TMP
            if loc in D:
                v=Vs[D[loc]]
                #errormat.append(er)
            else:
                D[loc]=len(Vs)
                Vs.append([0]*N_PAR)
                v=Vs[-1]
                errormat.append([er])
            date2=G.node[i]['created_at']
            deltad=diff_create(date,date2)
            
            a=G.node[i]['followed']
            #if a!=0:
            #    a=a**-0.25
            
            b=G.node[i]['followers']
            
            
            d=G.node[i]['connectivity']
            c=G.node[i]['jaccard_coef']
            #e=len(G)-1

            v[0]+=1
            v[1]+=c
            v[2]+=d
            #v[3]+=a
            v[3]+=deltad
            v[4]+=b
            #v[4]+=a
            
            for ite in range(N_PAR):
                if abs(MAXES[ite])<abs(v[ite]):
                    MAXES[ite]=abs(v[ite])
        #for i in range(len(Vs)):
            #Vs[i][0]=float(Vs[i][0])/float(Vs[i][1]) #take mean


        for i in range(len(Vs)):
            for j in range(N_PAR):
                if MAXES[j]==0:
                    print (Vs)
                    print (j)
                    print (MAXES)
                Vs[i][j]/=MAXES[j]
            Vs[i]=numpy.array(Vs[i])
            #Vs[i]=numpy.array([Vs[i]])
            #errormat[i]=numpy.array([errormat[i]])
            
        #return (numpy.array(Vs),numpy.array(errormat),wasfound)
        return (numpy.array(Vs),numpy.array(errormat),wasfound)


    
    return None

def flatten(data):
    ret=[]

    for i in data:
        #ret[0]=numpy.append(ret[0],[i[0]])
        #ret[0]+=list(i[0])
        
        for j in range(len(i[0])):
            ret.append((numpy.array([i[0][j]]),numpy.array([i[1][j]])))

        #ret[1]=numpy.append(ret[1],i[1])
        
        
        #ret[1]+=i[1]
    #ret[0]=numpy.array(ret[0])
    
    
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
            #data+=res[:2]
            data.append(res[:2])
        #data+=res[:2]
        #data[0]=numpy.append(data[0],res[0])
        #data[1]=numpy.append(data[1],res[1])
    #normalize(data,MAXSCORE)
    
    return data
        

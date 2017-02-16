import os
import networkx
import sys
from plotloc import load_py2_graph
def find_poi(st):
    '''finds poi given the file name'''
    #EX: 
    #USA_150705043_21_78.gpickle
    li=st.split("_")
    return int(li[1])


def iterate(path):
    dir=os.listdir(path)#"/Users/Peter/Work/Network/all_graphs")
    for p in dir:
        if sys.version_info < (3,0): #Python2 version
            poi=find_poi(p)
            G=networkx.read_gpickle(path+"/"+p)
            yield (G,poi)
        else:
            poi=find_poi(p)
            G=load_py2_graph(path+"/"+p)
            yield (G,poi)
    

        

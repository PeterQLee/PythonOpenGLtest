import networkx
import sys
def jaccard(f,poi_id):


    a=set()
    b=set()
    proportions={}
    for i in f.edges(poi_id):
        a.add(i[1])
    for i in a:
        b=set()
        for k in f.edges(i):
            b.add(k[1])
        
        proportions[i]=(len(a.intersection(b))/len(a.union(b)))
    return proportions
if __name__=="__main__":
    f=networkx.read_gpickle(sys.argv[1])
    poi_id=233984745
    print(jaccard(f,poi_id))


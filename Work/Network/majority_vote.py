import networkx
import sys

def norm(s):
    return anglisize(s).lower()
#                     comparison, non compared
def majority(G,poi_id,li_criteria,weights=None):
    #get majority vote given the listed criteria
    location={}
    
    for I in range(len(G.nodes())):
        i=G.nodes()[I]
        if weights:
            
            w=weights[I]
        else:
            w=1
        if i==poi_id:continue
        
        quitflag=False
        loc=()
        for j in li_criteria:
            if quitflag:break
            D=G.node[i]
            if 'lat' not in D['coordinates']:

                quitflag=True
                break
            for k in j:
                #if D[k]=='':
                if len(D[k])==0:
                    #print ('quit')
                    quitflag=True
                    break
                D=norm(D[k])
                #print (len(D))
                #loc+=(anglisize(g.node[i][j][k]).lower(),)
            if not quitflag:
                loc+=(D,)
        
        if quitflag:
            continue

        if loc in location:
            location[loc]+=w
        else:
            location[loc]=w

    return location

def anglisize(name):

    xlate= {
        0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y'}
    ##Taken from http://stackoverflow.com/questions/930303/python-string-cleanup-manipulation-accented-characters/930316#930316
    fin_str=""
    for i in name:
        if ord(i) in xlate:
            fin_str+=xlate[ord(i)]
        elif ('A' <= i and i <= 'Z') or ('a' <= i and i <= 'z'):
            fin_str+=i
            #otherwise ignore the character
        else: fin_str+=i
    return fin_str


def rank(di,i):
    #gets the top ranked locations, in order

    k= sorted(di,key=di.get,reverse=True)
    k=k[:i+1]
    if ('','') in k:
        #get rid of the useless no location string
        #print(k)
        k.remove(('',''))
        #print("REM")
        #print(k[:i])
    k=k[:i] #in case there was no empty
    
    J=[]
    for j in k:
        J.append((j,di[j]))

    return J

def resolve(placename):
    #todo, resolve so duplicate names have a single identity
    return placename

# def niave_majority(g,poi_id):
#     #just goes through all and puts them in a dictionary
#     location={}
#     for i in g.nodes():
#         if i==poi_id:continue
#         #Uncomment for city/ state
#         #if g.node[i]["city"]=="" or g.node[i]["state"]=="" or 'lng' not in g.node[i]["coordinates"]:
#         #    continue

#         #loc=(anglisize(g.node[i]["city"]).lower(),anglisize(g.node[i]["state"]).lower())

#         #Uncomment for state
#         if g.node[i]["state"]=="":
#            continue
#         loc=("".lower(),anglisize(g.node[i]["state"]).lower())

        
#         if loc in location:
#             location[loc]+=1
#         else:
#             location[loc]=1
#     return location

# def country_majority(g,poi_id):
#     location={}
#     for i in g.nodes():
#         if i==poi_id:continue

#         if g.node[i]["country"]=="":
#            continue
#         loc=anglisize(g.node[i]["country"]).lower()

        
#         if loc in location:
#             location[loc]+=1
#         else:
#             location[loc]=1
#     return location
    
# # def test_majority(g,poi_id):
# #     #just goes through all and puts them in a dictionary
# #     location={}
# #     for i in g.nodes():
# #         if i==poi_id:continue
# #         #uncomment for city/state
# #         if g.node[i]["city"]=="" or g.node[i]["state"]=="" or 'lng' not in g.node[i]["coordinates"]:
# #             continue
# #         #Uncomment for city/ state
# #         loc=(anglisize(g.node[i]["city"]).lower(),anglisize(g.node[i]["state"]).lower())

# #         #Uncomment for state
# #         #loc=("".lower(),anglisize(g.node[i]["state"]).lower())

# #         if loc in location:
# #             location[loc]+=1
# #         else:
# #             location[loc]=1
# #     return location

# def coord_majority(g,poi_id):
#     #just goes through all and puts them in a dictionary
#     location={}
#     for i in g.nodes():
#         if i==poi_id:continue
#         if g.node[i]["city"]=="" or g.node[i]["state"]=="" or 'lng' not in g.node[i]["coordinates"]:
#             continue
#         loc=(anglisize(g.node[i]["city"]).lower(),anglisize(g.node[i]["state"]).lower(),g.node[i]["coordinates"]['lng'],g.node[i]['coordinates']['lat'])

#         if loc in location:
#             location[loc]+=1
#         else:
#             location[loc]=1
#     return location

def binary_insert(li,tup):
    #binary search inserts
    bot=0
    top=len(li)-1
    i=(top-bot)//2
    found=False
    while not found:
        #print(i,top,bot)
        if li[i][1]<tup[1]:
            top=i-1
        elif li[i][1]>tup[1]:
            bot=i+1
        if (top<bot) or li[i][1]==tup[1]:
            li.insert(i,tup)
            found=True            
        i=(top+bot)//2

    return li[0:len(li)-1]
    
def kth_nearest(g,poi_id,k):
    #gives the kth nearest neighbours based on the specified weight.
    #returns a list of tuples consisting of the id and the weight
    order_li=[(0,0)]*k
    closest_li=[]

    for i in g.edges(poi_id,data=True):
        if (order_li[k-1][1]<i[2]['weight']):
            tup=(i[1],i[2]['weight'])
            #binary insert
            order_li=binary_insert(order_li,tup)
    #print (order_li)
    for i in order_li:
        closest_li.append((i[0],i[1]))
    return closest_li

    

def list_majority(li,G):
    loc={}
    for i in li:
        #location=(G.node[i]["city"].lower(),G.node[i]["state"].lower())
        location=("".lower(),anglisize(G.node[i]["state"]).lower())
        if location in loc:
            loc[location]+=1
        else:
            loc[location]=1
            #sorted_x=sorted(loc.items(),key=operator.itemgetter(1),reverse=True)
    return loc



1
    
if __name__=="__main__":
    g=networkx.read_gpickle(sys.argv[1])
    poi_id=0
    print (g.nodes())
    for i in g.nodes():
        if i==150705043:
            poi_id=i
            break

    t=niave_majority(g,poi_id)
    print (t)
    print (rank(t,5))



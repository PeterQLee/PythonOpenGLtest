#import tweepy
import networkx
#import secrets
import sys
import time

#def Authorize(secrets):
#    auth=tweepy.OAuthHandler(secrets.consumer_key,secrets.consumer_secret)
#    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
#    return auth

#  #def node_neighbours(api,_id):
# #    #get the neighbours of poi
# #    ret=[]
#     while len(ret)==0:
#         try:
#             api.followers_ids(_id)
#         except tweepy.TweepError:
#             print("limit error, waiting 15 minutes")
#             time.sleep(15*60)
#     return ret

if __name__=="__main__":
    
   # try:

    g=networkx.read_gpickle(sys.argv[1])
    #except:
     #   print(sys.argv[1]+" File not found")
    b=len(g.nodes())-1
    poi=0
    for i in g.nodes():
        if g.node[i]["poi"]=='Y': #not a poi, explore neighbours
            poi=i
    for i in g.nodes():
        
        if g.node[i]["poi"]=='N': #not a poi, explore neighbours

            a=len(g.neighbors(i))
            g[i][poi]["weight"]=a/b
            
    
    
    #write the new graph
    networkx.write_gpickle(g,"new"+sys.argv[1])
    
            
            
            
    
    
    






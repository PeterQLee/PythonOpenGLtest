#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
import networkx
import numpy as np
import sys


# def draw(coords, path='../testtwitter/Location/bound_p'):
    
#     width = 28000000; lon_0 = -105; lat_0 = 40
#     m = Basemap(llcrnrlon=-167.45,llcrnrlat=24.5,urcrnrlon=-52.16,urcrnrlat=83.28,
#                 projection='cyl',lat_1=33,lat_2=45,lon_0=-95)

#     m.drawcoastlines(linewidth=0.5)


#     m.readshapefile(path, name='bounds', drawbounds=True,default_encoding="windows-1252")
#     for x_,y_ in coords:
#         x,y=m(x_,y_)
#         m.plot(x,y,marker='D',color='m')
#     plt.show()

def load_py2_graph(target):
    G=networkx.read_gpickle(target,fix_imports=True,encoding="bytes")
    #Python 2 to 3 hack
    
    G.node=G.__dict__[b'node']
    keys=list(G.node[G.nodes()[0]].keys())

    for i in G.node:
        for k in keys:
            regk=k.decode('utf-8')
            try:
                G.node[i][regk]=G.node[i][k]
                del G.node[i][k]
            except:
                pass
        try:
            G.node[i]['coordinates']['lat']=G.node[i]['coordinates'][b'lat']
            G.node[i]['coordinates']['lng']=G.node[i]['coordinates'][b'lng']
            del G.node[i]['coordinates'][b'lat']
            del G.node[i]['coordinates'][b'lng']
        except:
            if G.node[i]['coordinates']!={}:
                print (G.node[i]['coordinates'])
    G.graph=G.__dict__[b'graph']
    G.adj=G.__dict__[b'adj']
    G.edge=G.__dict__[b'edge']

    del G.__dict__[b'node']
    del G.__dict__[b'graph']
    del G.__dict__[b'adj']
    del G.__dict__[b'edge']

    return G

if __name__=='__main__':
    target="USA_1271636977_21_177.gpickle"

    load_py2_graph('graphs/'+target)
    coord_list=[]
    for i in G.node:
        coord=G.node[i][b"coordinates"]
        if b'lat' in coord : #check if valid coord

            coord_list.append((coord[b'lng'],coord[b'lat']))
    print (coord_list)
    draw(coord_list)
    

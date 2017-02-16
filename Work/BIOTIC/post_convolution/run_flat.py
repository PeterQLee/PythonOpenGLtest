import csv
import numpy as np
from smoothing import gaussian_kernel
import sys
sys.path.insert(0,'../Prob_mapgen/')
from create_images import find_crop, create_images
f=np.load(sys.argv[1])
data=csv.reader(open('../Data/4secmodel.csv','r'))
coords=csv.reader(open('../Data/4secmodelcoords.csv','r'))
vals=data.__next__()
cs=coords.__next__()
M=np.zeros((512,512,35))

conv=lambda x: (x//512,x%512)
c=0
suffix=sys.argv[1].split('/')[-1].split('.')[0]

while c < len(f):
    vals=data.__next__()
    cs=coords.__next__()
    if vals[5]!=suffix:continue

    sl=int(vals[4])
    x,y=conv(int(cs[0]))
    if len(f.shape)==1 or f.shape[1]==1:
        M[x,y,sl]=int((1-f[c])*255) #Correction for how I processed it earlier
    else:
        M[x,y,sl]=int(f[c,1]*255)
    c+=1


res1=[]
res2=[]
#for sigma in np.arange(0,10,0.3):
sigma=2.5
Mn=gaussian_kernel(np.copy(M),sigma)
#Get accuracy
hits=[0,0]
tot=[0,0]

refF=np.load('../Data/4secmodel.npz')
ref=refF[suffix+'_label']
for z in range(35):
    bounds=find_crop(ref[:,:,z])
    for x in range(bounds[0],bounds[1]):
        for y in range(bounds[2],bounds[3]):
            if ref[x,y,z,0]>0:
                tot[0]+=1
                if Mn[x,y,z]<0.5*255:
                    hits[0]+=1
            elif ref[x,y,z,1]>0:
                tot[1]+=1
                if Mn[x,y,z]>0.5*255:
                    hits[1]+=1
#res1.append(hits[0]/tot[0])
#if (tot[1]==0): res2.append(0)
#else:res2.append(hits[1]/tot[1])

# import matplotlib.pyplot as plt
# plt.plot(np.arange(0,10,0.3),res1,c='b')
# plt.plot(np.arange(0,10,0.3),res2,c='r')

# plt.xlabel('Sigma')
# plt.ylabel('Accuracy')
# plt.title('Accuracy for sigma of gaussian kernel (blue is non-cancer')
# plt.show()
print ('Accuracies',hits[0]/tot[0],hits[1]/tot[1])

create_images(Mn,ref,suffix,sys.argv[2])

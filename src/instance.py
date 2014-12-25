import tools #not sure if this will be included

class instance:
    def __init__(self, stackname): #note, in future, this will load maps and stuff in lists
        
        self.name=stackname
        if not self.readStack():
            
            self.lettermap=[]
            self.height=[]
            self.width=[]
            self.colorsize=1 #linear
            self.curcharid=[1] #Char ids will be the same for file {0, 58, and 44 are forbidden values}
            #note curchar is opposite so ind 0 is the first digit that is changing
            
            #wll need to make charids an array... or use moduluses...
            self.colormap={} ##in the future, map have color map be predetermined by file
            #that way file can be more compressed
        
            self.numImage=0
            #will predetermine size, so can just be a singular list of values
    def newImage(self,sizex,sizey):
        #in real version, will create new index in all lists
        #self.curcharid.append(1)
        self.numImage+=1
        n=self.numImage-1
        self.height.append(sizey)
        self.width.append(sizex)
        #self.colorsize=1
        self.colormap[chr(1)]=tools.converthex("#FFFFFF")
        self.lettermap.append(chr(1)*self.width[n]*self.height[n]*self.colorsize)
        
        
    def getDimensions(self,index):
        return (self.width[index],self.height[index]) #x,y
    
    def getRGBMap(self,index):
        h=self.height[index]
        w=self.width[index]
        cs=self.colorsize
        offset=3
        RGBA=[0]*h*w*offset
        for y in range(h):
            for x in range(w):
                start=y*w*offset+x*offset#int(x/cs)*offset
                letterpos=y*w*cs+x*cs
                RGBA[start:start+offset]=self.colormap[self.lettermap[index][letterpos:letterpos+cs]] #check this
        return RGBA

    def updateImage(self,index,li):
        print(len(li))
        sn=""
        for k in range(0,len(li),3):
            #print(k)
            R=li[k]
            G=li[k+1]
            B=li[k+2]
            alright=False #flag for if colour is already mapped
            s=-1
            for i in self.colormap.keys():
                if self.colormap[i]==[R,G,B]:
                    alright=True
                    
                    #s=ord(i)
                    s=i
                    break
            #print("what")
     
            if not alright:
                self.curcharid[0]+=1
                if self.curcharid[0]==44 or self.curcharid[0]==58:self.curcharid[0]+=1
                #check if every character is 255
                yes255=True
                for u in self.curcharid:
                    if u!=255:
                        yes255=False
                        break
                if yes255:  #right here we are just saying when the first is 255, not when it overflows... needs work
                    #if all curcharid==255..
                    self.reFormatMap()
                alm=""
                for k in range(len(self.curcharid)-1,-1,-1):
                    alm+=chr(self.curcharid[k]) ##check right here
                self.colormap[alm]=[R,G,B]#
                s=alm
            #print('k')
            #print(s)
            sn+=s#chr(s)
            #print("may?")
        self.lettermap[index]=sn
        print("done")
    def saveStack(self):
        """
        format:
        numimage:colormap::heights(sep by,):widths(sep by,):colorsize:(the map)
        """
        print ("imawork")
        f=open(self.name+".qcard","w")
        f.write(str(self.numImage)+":")
        
        f.write(str(self.colorsize))
        f.write(":")
        for i in self.colormap.items():
            f.write(str(i[0])+","+str(i[1][0])+","+str(i[1][1])+","+str(i[1][2])+",") #obviously in future a better way will be used
        f.write(":")
        for i in self.height:
            f.write(str(i)+",")
        f.write(":")
        for i in self.width:
            f.write(str(i)+",")
        f.write(":")
        
        
        for i in self.lettermap:
            f.write(i+",") #we will have to change this | seperator...
        f.write(":")
        f.close()
    def readStack(self):
        f=None
        try:
            f=open(self.name+".qcard","r")
        except:
            return False
        s="n"
        stage=0 #0=num image, 1=colorsize, 2=colormap, 3=height, 4=width, 5=lettermap
        buffer=""
        
        while True:
            #print(stage)
            #print(buffer,"stage:",stage)
            s=f.read(1)
            if s==":": #and (stage==0 or stage==1 or stage==3 or stage==4):
                if stage==0:
                    self.numImage=int(buffer)
                if stage==1:
                    self.colorsize=int(buffer)
                if stage==2:
                    d=buffer.split(",")
                    dic={}
                    high=0
                    ms=[]
                    for i in range(0,len(d)-1,4): 
                        dic[d[i]]=[int(d[i+1]),int(d[i+2]),int(d[i+3])]
                        val=0
                        for o in range(len(d[i])-1,-1,-1):#reverse this!
                            val+=ord(d[i][o])*pow(255,len(d[i])-1-o)
                        oldhigh=high
                        high=max(high,val)
                        if high!=oldhigh:
                            ms=[]
                            for r in d[i]:
                                ms.insert(0,ord(r)) #will reverse order i think
                            
                    self.colormap=dic
                    self.curcharid=ms
                if stage==3:
                    d=buffer.split(",")
                    li=[int(i) for i in d[:len(d)-1]]
                    self.height=li
                if stage==4:
                    d=buffer.split(",")
                    fi=[int(i) for i in d[:len(d)-1]]
                    self.width=fi
                if stage==5:
                    d=buffer.split(",")
                    self.lettermap=d[:len(d)-1]
                    break
                stage+=1
                buffer=""
                continue
            
            buffer+=s
        
        return True

    def reFormatMap(self):
        
        key=self.colormap.keys()
        newdic={}
        repdic={}
        for i in key:
            newdic[chr(0)+i]=self.colormap[i]
            repdic[i]=chr(0)+i
        self.colormap=newdic
        #redind thing
        n=self.colorsize
        self.colorsize+=1
        self.curcharid=[chr(0)]*n+[chr(1)]#[chr(1)]+[chr(0)]*(n)
        #reformat lettermap
        newarr=[]
        for i in self.lettermap:
            dastr=""
            for j in range(0,len(i),n):
                dastr+=repdic[i[j:j+n]] #here
            newarr.append(dastr)
        self.lettermap=newarr
    #too slow
    
    """
    def mouseChange(self,x,y,R,G,B,A,index):#not sure about alpha
        alright=False #flag for if colour is already mapped
        for i in self.colormap.keys():
            if self.colormap[i]==[R,G,B]:#,A]:
                alright=True
        if not alright:
            self.curcharid[index]+=1
            self.colormap[chr(self.curcharid[index])]=[R,G,B]#,A]
        ind=x*self.colorsize[index]+y*self.width[index]*self.colorsize[index]
        self.lettermap[index]=self.lettermap[index][:ind]+chr(self.curcharid[index])+self.lettermap[index][ind+self.colorsize[index]:]"""
        
            

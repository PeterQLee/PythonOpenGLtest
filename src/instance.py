import tools #not sure if this will be included

class instance:
    def __init__(self, stackname): #note, in future, this will load maps and stuff in lists
        self.name=stackname
        #self.colormapold=[{"A":"#000000","B":"#444444"}] #character range will be anywhere between chr(0) to chr(255), after that, additional characters will be created
        self.lettermap=[]
        self.height=[]
        self.width=[]
        self.colorsize=[]
        self.curcharid=[] #In future, char ids will be the same for the file
        self.colormap={} ##in the future, map have color map be predetermined by file
        #that way file can be more compressed
        
        self.numImage=0
        #will predetermine size, so can just be a singular list of values
    def newImage(self,sizex,sizey):
        #in real version, will create new index in all lists
        self.curcharid.append(1)
        self.numImage+=1
        n=self.numImage-1
        self.height.append(sizey)
        self.width.append(sizex)
        self.colorsize.append(1)
        self.colormap[chr(self.curcharid[n])]=tools.converthex("#00FFFF")
        self.lettermap.append(chr(self.curcharid[n])*self.width[n]*self.height[n]*self.colorsize[n])
        
        
    def getDimensions(self,index):
        return (self.width[index],self.height[index]) #x,y
    
    def getRGBMap(self,index):
        h=self.height[index]
        w=self.width[index]
        cs=self.colorsize[index]
        offset=3
        RGBA=[0]*h*w*offset
        for y in range(h):
            for x in range(w):
                start=y*w*offset+int(x/cs)*offset
                letterpos=y*w*cs+x*cs
                RGBA[start:start+offset]=self.colormap[self.lettermap[index][letterpos:letterpos+cs]] #check this
        return RGBA       
    def mouseChange(self,x,y,R,G,B,A,index):#not sure about alpha
        alright=False #flag for if colour is already mapped
        for i in self.colormap.keys():
            if self.colormap[i]==[R,G,B]:#,A]:
                alright=True
        if not alright:
            self.curcharid[index]+=1
            self.colormap[chr(self.curcharid[index])]=[R,G,B]#,A]
        ind=x*self.colorsize[index]+y*self.width[index]*self.colorsize[index]
        self.lettermap[index]=self.lettermap[index][:ind]+chr(self.curcharid[index])+self.lettermap[index][ind+self.colorsize[index]:]
        
            

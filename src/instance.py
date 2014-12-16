import tools #not sure if this will be included

class instance:
    def __init__(self, stackname):
        self.name=stackname
        self.li=[255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                 255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,255,0,0]
        self.colormapold={"A":"#000000","B":"#444444"} #character range will be anywhere between chr(0) to chr(255), after that, additional characters will be created
        self.lettermap="AABBAA"
        self.height=3
        self.width=2
        self.colorsize=1
        self.colormap={"A":tools.converthex("#000000"),"B":tools.converthex("#444444")}
        
        #will predetermine size, so can just be a singular list of values
        
    def getPixmap(self): #DEPRICATE
        return self.li
    def getColormap(self): #DEPRICATE
        return self.colormapold
    def getRGBMap(self):
        RGBA=[0]*self.height*self.width*4
        for y in range(self.height):
            for x in range(self.width):
                start=y*self.width*4+int(x/self.colorsize)*4
                letterpos=y*self.width*self.colorsize+x*self.colorsize
                RGBA[start:start+4]=self.colormap[self.lettermap[letterpos:letterpos+self.colorsize]] #check this
        return RGBA       
        

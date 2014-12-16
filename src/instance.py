
class instance:
    def __init__(self, stackname):
        self.name=stackname
        self.li=[255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                 255,0,0,255,0,0,255,0,0,255,0,0,255,0,0,255,0,0]
        self.colormap={"A":"#000000","B":"#444444"}
        
        #will predetermine size, so can just be a singular list of values

    def getPixmap(self):
        return self.li
    def getColormap(self):
        return self.colormap
    

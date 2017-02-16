
def converthex(string):#in the future may add opaque feature
    li=[0,0,0]#,0] excluding alpha for now
    li[0]=int(string[1:3],16)
    li[1]=int(string[3:5],16)
    li[2]=int(string[5:7],16)
    return li

import numpy as np
from scipy.special import expit
import matplotlib.pyplot as plt
import random
import vectorize_graph
def f(x):
    #correct output
    return x**2

def sigmoid(x,deriv=False):
    if deriv:
        y=sigmoid(x)
        return y*(1-y)
    #print (-x)
    return expit(x)
    #return 1/(1+np.exp(-x))

def squash(x):
    pass

def over(x,y):
    if y>x**2:
        return 1
    return 0
def func(x_):
    #x=np.array([[x_],[y]])
    x=np.array([x_]).T
    a_2=sigmoid(np.dot(w_2,x)+biases_2)
        
    #a_3=sigmoid(np.dot(w_3,a_2)+biases_3)
    
    a_4=sigmoid(np.dot(w_4,a_2)+bias4)

    return a_4

np.seterr(over='raise')
np.random.seed(7)

Bdata=vectorize_graph.vectorize_graph('../graphs_all/')
data=vectorize_graph.flatten(Bdata)
x_set=data[0]
out_set=data[1]

data_sep=600 #Used for seperating training and test data

training=Bdata[:data_sep]#list(zip(x_set,out_set))
N_PAR=len(Bdata[0][0][0])
print (N_PAR)

print (len(training))
#x=np.array([[1],[2],[3],[4],[5],[6],[7]])
#y_set=np.square(x_set)#5*x_set+3
#y_set=y_set/np.linalg.norm(y_set)

w_2=np.random.randn(50,N_PAR) #Order is (output, input) i.e. (to, from)
#w_3=np.random.random((8,8))
w_4=np.random.random((1,50))
biases_2=np.random.random((50,1))
#biases_3=np.random.random((8,1))
bias4=np.random.random((1,1))
hits=0

mini_batch_size=4

EPOCHS=300


eval_data=Bdata[data_sep:]

for i in range(EPOCHS):
    #input
    random.shuffle(training)
    mini_batches=[training[k:k+mini_batch_size]
                  for k in range(0,len(x_set),mini_batch_size)]
    
    for mini_batch in mini_batches:
        #for x_,y,z in mini_batch:
        for mB in mini_batch:

            X_=mB[0]
            Z=mB[1]
            for mBB in range(len(mB[0])):
                #print (mB[0])
                if True:
                #for X_,Z in mB:

                    x_=X_[mBB]
                    z=Z[mBB]

                    x=np.array([x_]).T#np.array([[x_],[y]])
                    #print (x.shape)                
                    #feed forward
                    
                    a_2=sigmoid(np.dot(w_2,x)+biases_2)
                    
                    #a_3=sigmoid(np.dot(w_3,a_2)+biases_3)
                    
                    a_4=sigmoid(np.dot(w_4,a_2)+bias4)

                    if z==0:
                        error=a_4-z/(len(mB[0])-1)
                    else:
                        error=a_4-z
                    
                    #calculate output error
                    delta_4=(error)*sigmoid(np.dot(w_4,a_2)+bias4) #aka, delta L
                
                    #back propagate
                    #delta_3=np.dot(w_4.transpose(),delta_4)*sigmoid(np.dot(w_3,a_2)+biases_3,True)
                    
                    delta_2=np.dot(w_4.transpose(),delta_4)*sigmoid(np.dot(w_2,x)+biases_2,True)

                    #5. Output
                    #calculate dC/dw_l,jk and dC/db_l,j

                    delta_nabla_4W=np.dot(delta_4,a_2.transpose()) #need to make sure right matrix is transposed!
                    delta_nabla_4B=delta_4
                    
                    #delta_nabla_3W=np.dot(delta_3,a_2.transpose())
                    #delta_nabla_3B=delta_3
                
                    delta_nabla_2W=np.dot(delta_2,x.transpose())
                    delta_nabla_2B=delta_2
                    #updat weights
                    learnrate=3/len(mB[0])
                    #learnrate=3/len(minibatch)
                    w_4-=delta_nabla_4W*learnrate
                    bias4-=delta_nabla_4B*learnrate
                    #w_3=w_3-delta_nabla_3W*learnrate
                    #biases_3-=delta_nabla_3B*learnrate
                    w_2=w_2-delta_nabla_2W*learnrate
                    biases_2-=delta_nabla_2B*learnrate

    if (i+1)%50==0:
        c=0
        w=len(Bdata)
        G=np.vectorize(func)
        mv=0
        for i in Bdata:
            maj=[]
            tt=[]
            for m in range(len(i[0])):
                ghde=func(np.array(i[0][m]))
                #print (np.array([i[0][m]]).shape)
                #print (ghde.shape)
                maj.append(i[0][m][0])
                tt.append(ghde)

            if np.argmax(tt)==np.argmax(i[1]):
                c+=1
            if np.argmax(i[1])==np.argmax(maj):
                mv+=1
        print ("Result is "+str(c/w))
        print ("Majoirty Result was "+str(mv/w))
                #Try evaldata

        c=0

        w=len(eval_data)
        mv=0
        for i in eval_data:

            tt=[]
            maj=[]
            for m in range(len(i[0])):
                ghde=func(np.array(i[0][m]))

                tt.append(ghde)
                maj.append(i[0][m][0])

            if np.argmax(tt)==np.argmax(i[1]):
                c+=1
            if np.argmax(i[1])==np.argmax(maj):
                mv+=1


        print ("Eval result is "+ str(c/w))
        print ("Maj result was "+ str(mv/w))



#space=x_set
print (w_2)
print (w_4)

#y=G(x_set)#G(x_set,y_set)
#z=over(x_set,y_set)#5*space+3
#z=z/np.linalg.norm(z)
#print(y)
#z=np.square(x_set)
#plt.plot(x_set,z,'-')
y=[]
for m in range(len(x_set)):
    y.append(func(x_set[m]))

print (len(x_set), len(out_set), len(Bdata))
plt.scatter([i[0] for i in x_set],out_set,c=y,s=20)
plt.gray()
#plt.plot(space,y_set,'-')
plt.show()

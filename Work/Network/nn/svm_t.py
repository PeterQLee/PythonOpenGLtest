from sklearn import svm
import vectorize_graph
import numpy

Bdata=vectorize_graph.vectorize_graph('../graphs_all/')
data=vectorize_graph.flatten(Bdata[:500])
print (data[0][0])
x_set=[data[i][0].flatten() for i in range(len(data))]
y_set=numpy.array([data[i][1].flatten() for i in range(len(data))]).flatten()
clf=svm.SVC(probability=True)
clf.fit(x_set,y_set)


eval_data=Bdata[450:]
w=len(eval_data)
c=0
mc=0
for i in eval_data:
    x=i[0]
    o=clf.predict(x)
    
    y=i[1]
    if numpy.argmax(o)==numpy.argmax(y):
        c+=1
    if numpy.argmax([j[0] for j in x])==numpy.argmax(y):
        mc+=1
print ("Eval data score is: ",c/w)
print ("MV score is ",mc/w)

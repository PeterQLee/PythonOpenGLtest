import tensorflow as tf
import vectorize_graph
import numpy
import random

tf.set_random_seed(7)
# Parameters
learning_rate = 0.001
training_epochs = 100
#batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 3 # 1st layer number of features
n_hidden_2 = 3 # 2nd layer number of features
n_input = 5 # MNIST data input (img shape: 28*28)
n_classes = 1 # MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])


def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    
    #layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    #layer_2 = tf.nn.relu(layer_2)
    
    # Output layer with linear activation
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    out_layer=tf.nn.sigmoid(out_layer)
    return out_layer
    



weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

tf_threshold=tf.Variable(0.8)


# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
#cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(pred, y))
cost = tf.reduce_mean(tf.square(pred-y))

#cost= tf.reduce_mean(tf.nn.softmax(pred))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.initialize_all_variables()
cursor=0
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    D=vectorize_graph.vectorize_graph('../graphs_all/')
    U=vectorize_graph.flatten(D[:450])
    data=U

    total_batch=len(data)
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        #total_batch = int(len(data)/batch_size)
        # Loop over all batches
        random.shuffle(data)
        cursor=0
        #for i in range(len(data)):
        while cursor< len(data):
            #batch_x, batch_y = mnist.train.next_batch(batch_size)
            
            #if cursor>total_batch:
            #    random.shuffle(data)
            #    cursor=0
            
            #batch_x,batch_y=data[cursor:cursor+20]
            batch_x=numpy.array([i[0] for i in data[cursor:cursor+20]])
            #print(batch_x)
            batch_y=numpy.array([i[1] for i in data[cursor:cursor+20]])

            #batch_y=data[1][cursor:cursor+20]
            cursor+=20
            # Run optimization op (backprop) and cost op (to get loss value)
            ctot=0
            for i in range(len(batch_x)):
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x[i],
                                                              y: batch_y[i]})
                ctot+=c
            # Compute average loss
            #tf.Print(weights['h1'],[weights['h1']])
            avg_cost += c / total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print( "Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost))
    print ("Optimization Finished!")

    #tot=0
    #for i in D[50:]:
    #    true_count+=(eval_correct, feed_dict=feed_dict)
    
    # Test model
    eval_dat=D[450:]#[:50]
    tot=0
    c_w=0
    for i in range(len(eval_dat)):
        #b_x=numpy.append(b_x,eval_dat[i][0],axis=0)
        #b_y=numpy.append(b_y,eval_dat[i][1],axis=0)
        b_x=eval_dat[i][0]#numpy.array([i[0] for i in eval_dat])
        #print(b_x.shape)
        #b_x=eval_dat[i][0]
        b_y=eval_dat[i][1]#numpy.array([i[1] for i in eval_dat])
        #b_y=eval_dat[i][1]

        correct_prediction=tf.equal(tf.argmax(pred,0),tf.argmax(y,0))
        #correct_prediction=tf.argmax(pred,0)#tf.greater_equal(pred,tf_threshold)
    
        #c=pred.eval({x:b_x,y:b_y})
        #print (c)
 #      c=tf.argmax(pred,0).eval({x:b_x,y:b_y})

        c=correct_prediction.eval({x:b_x,y:b_y})

        tot+=1
        if c[0]==True and numpy.count_nonzero(b_y)!=0:
            c_w+=1
        #if c[0]==True:break

    print( c_w/tot)

    # print (b_y.shape)
    # correct_prediction = tf.equal(tf.argmax(pred, 1), y)
    # # Calculate accuracy
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    # print ("Accuracy:", accuracy.eval(feed_dict={x:b_x , y:b_y }))





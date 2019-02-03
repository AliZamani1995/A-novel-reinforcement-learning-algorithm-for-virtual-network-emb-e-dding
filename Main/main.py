#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:44:41 2019

@author: ali
"""
import sys
sys.path.insert(0, '../ReadFile')
sys.path.insert(0, '../MFMatrix')
sys.path.insert(0, '../Given')
import InputConstants
from InputConstants import Inputs
from ReadFile import Graph, Chains
import tensorflow as tf
from mfMatrix import Mf
import numpy as np
input_cons = InputConstants.Inputs()

#graph = Graph('../Data/nsf_14_network.json')
#_chain = Chains('../Data/nsf_14_network.json')

graph = Graph(input_cons.network_path + input_cons.network_name)
_chain = Chains(input_cons.chains_path + input_cons.chains_name, graph)
chains = _chain.read()

#_chain.function_cpu_usage(1)
#graph.function_placement(node=2, ser='WebService', fun='ali1')
#graph.function_placement(node=2, fun='ali')
#%%
#mf = Mf(graph)
graph.get_feature_matrix()
#mf.function_placement(node=2, ser='WebService', fun='ali')
#
#mf.function_placement(node=2, ser='WebService', fun='ali1')
#%%
#graph.floydWarshall()  
  

#%%
# Learning

node_num = len(graph.node_list)
# Def.ine placeholder x for input
x = tf.placeholder(dtype=tf.float64, shape=[node_num, input_cons.node_features], name="x")
# Define placeholder y for output
y = tf.placeholder(dtype=tf.float64, shape=[1, node_num], name="y")
# Define variable w and fill it with random number
w = tf.Variable(tf.random_normal(shape=[input_cons.node_features, 1], stddev=0.1, dtype=tf.float64), name="weights", dtype=tf.float64, trainable=True)
# Define variable b and fill it with zero 
b = tf.Variable(tf.zeros(1, dtype=tf.float64), name="bias", dtype=tf.float64, trainable=True)
# Fetch a list of our network's trainable parameters.
trainable_vars = tf.trainable_variables()
# Create variables to store accumulated gradients
## initialize
#tf.local_variables_initializer().run()
#tf.global_variables_initializer().run()




#accumulators = [
#    tf.Variable(
#        tf.zeros_like(tv.initialized_value()),
#        trainable=False
#    ) for tv in trainable_vars
#]





#print(accumulators)
# Define logistic Regression
logit = tf.matmul(x, w) + b
logit_mod = tf.reshape(logit, [1, -1])
#_sum = tf.reduce_sum(logit)
#y_predicted = tf.exp(logit[0])/(1+_sum)
y_predicted = tf.nn.softmax(logit_mod)
#y_predicted1 = 1.0 / (1.0 + tf.exp(-logit))
# Define maximum likelihood loss function
loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=logit_mod, labels=y)
cost = tf.reduce_mean(loss)
# Define optimizer: GradientDescent         
optimizer = tf.train.GradientDescentOptimizer(learning_rate= input_cons.learning_rate)

# Compute gradients; grad_pairs contains (gradient, variable) pairs
grad_pairs = optimizer.compute_gradients(loss, [w, b])
# Create operations which add a variable's gradient to its accumulator.
#%%
#accumulate_ops = [
#    accumulator.assign_add(
#        grad
#    ) for (accumulator, (grad, var)) in zip(accumulators, grad_pairs)
#]
#%%
#train_step = optimizer.apply_gradients(
#    [(accumulator, var) 
#        for (accumulator, (grad, var)) in zip(accumulators, grad_pairs)]
#)
# Accumulators must be zeroed once the accumulated gradient is applied.
#zero_ops = [
#    accumulator.assign(
#        tf.zeros_like(tv)
#    ) for (accumulator, tv) in zip(accumulators, trainable_vars)
#]                                                
opt = optimizer.minimize(cost)
init = tf.initialize_all_variables()
#%%
#grad = optimizer.compute_gradients(cross_entropy, w)
#gradients = [g for g, variable in grad]
#gradients, variable = zip(*grad)

#optimize = optimizer.apply_gradients(zip(gradients, variable))
#gradients1 = gradients[0]
#gradi_list = tf.zeros(input_cons.node_features)
#gradi_sum = tf.zeros(input_cons.node_features)
#        
#for i in range(input_cons.node_features):
#    tf.assign(gradi_list[i], gradients1[i][0])
#gradi_sum += gradi_list
#grads_and_vars = optimizer.compute_gradients(cross_entropy)
#gradients = [grad for grad, variable in grads_and_vars]
#gradient_placeholders = []
#grads_and_vars_feed = []
#for grad, variable in grads_and_vars:
#    gradient_placeholder = tf.placeholder(tf.float32, shape=grad[0].shape())
#    gradient_placeholders.append(gradient_placeholder)
#    grads_and_vars_feed.append((gradient_placeholder, variable))
#training_op = optimizer.apply_gradients(grads_and_vars_feed)

#training_op = optimizer.apply_gradients(grad)
# Session
trainAccList = []
testAccList = []
trainErrList = []
testErrList = []
#for s in range(len(chains)):
#    for f in range(len(chains[s].fun)):
#        fun = chains[s].fun[f]
#%%  

accumulators = [
    tf.Variable(
        tf.zeros_like(tv.initialized_value()),
        trainable=False
    ) for tv in [w, b]
    ]
#%%
      
accumulate_ops = [
    accumulator.assign_add(
        grad 
    ) for (accumulator, (grad, var)) in zip(accumulators, grad_pairs)
                    ]

#mul_reward_acc = tf.multiply(accumulators, 0.1)
accumulate_mul = [
    accumulator.assign_add(
        accumulator * graph.rev_to_cost_val - accumulator  
    ) for (accumulator, (grad, var)) in zip(accumulators, grad_pairs)
                    ]
#multiply = tf.math.scalar_mul(tf.constant(0.1, dtype=tf.float32), accumulators)
#%%    
    
train_step = optimizer.apply_gradients(
    [(accumulator, var) 
        for (accumulator, (grad, var)) in zip(accumulate_mul, grad_pairs)]
                        )

zero_ops = [
    accumulator.assign(
        tf.zeros_like(tv)
    ) for (accumulator, tv) in zip(accumulators, [w, b])
                ]
#%%      
with tf.Session() as sess:
#    init.run()
# Fetch a list of our network's trainable parameters.
    
#    for tv in trainable_vars:
#        print(tv)
#    print(trainable_vars)
    tf.local_variables_initializer().run()
    tf.global_variables_initializer().run()



                    
    
                                              

    for epoch in range(input_cons.epoch_num):
        placed_chains = []
        graph.make_empty_nodes()
        reward_list = []
#    for epoch in range(20):
        #        gradi_list = np.zeros(input_cons.node_features)
#        gradi_sum = np.zeros(input_cons.node_features)

        
        grads_stack = 0
        cnt = 0
        for ser_num, s  in enumerate(chains):
            node_fun = []
            ser_name = s.name
            loss_list = []
#            print(ser_name)
#            fun = chains[s].fun[f]        
            grad_stack = np.zeros([1, input_cons.node_features], dtype=np.float)
            for fun in chains[ser_num].fun:
                graph.update_feature_matrix(node_fun)
            #    for epoch in range(1):
#                train_loss = 0

#                logit_RL = sess.run(logit, feed_dict={x: mf.mf_matrix})
                y_RL = sess.run(y_predicted, feed_dict={x: graph.mf_matrix})
                y_one_hot, candidate = graph.select_one(y_RL,
                                                     approach='sample')
#                print(y_one_hot)
                loss_list.append(sess.run(cost, feed_dict={y:y_RL , x: graph.mf_matrix}))
                                                       
#                print (gradi)
#                InputList = {x: mf.mf_matrix}
                
                gradients_val = sess.run(accumulate_ops, feed_dict={x: graph.mf_matrix, y: y_one_hot})
#                print(sess.run(grad_pairs, feed_dict={x: graph.mf_matrix, y: y_one_hot}))
#                gradients_val1 = sess.run(gradients1, feed_dict={x: graph.mf_matrix, y: y_one_hot})                                                    
#                print('*****')
#                print(gradients_val)
#                print('---------------------')
#                grad_stack = gradients_val[0] + grad_stack

#                grad_stack = grad_stack[:, 0]
#                print(grad_stack)
                node_fun.append((candidate, fun))   
#                print(graph.mf_matrix)
#                print(gradients_val)
#            print(node_fun)
#            print(gradients_val)
            if (graph.node_is_mapped(node_fun, chains) & 
                graph.link_is_mapped(node_fun)):
                reward = 0.001
                # multipy gradients
#                print
#                print(sess.run(accumulate_mul))
                graph.rev_to_cost(node_fun, ser_num, chains)
                print(graph.rev_to_cost_val)
                reward_list.append(graph.rev_to_cost_val)
                placed_chains.append(node_fun)
#                grads_stack += (input_cons.learning_rate * reward 
#                               * grad_stack) 
            else:
                placed_chains = []
                sess.run(zero_ops, feed_dict={x: graph.mf_matrix, y: y_one_hot})
                cnt = 0
#                grads_stack = 0
            cnt += 1
            if cnt == input_cons.batch_Size:
                #apply gradients
                accu = sess.run(accumulators)
                gr = sess.run(train_step)
#                print(sess.run(cost, feed_dict={x: graph.mf_matrix, y: y_one_hot}))
                w_val, b_val = sess.run([w, b])
                print(w_val)
                graph.batch_function_placement(ser_name, placed_chains)
                placed_chains = []
#                print('***************')
#                print(sess.run(accumulators))
#                print("--------------------------------------")
#                cost_ = sess.run(cost, feed_dict={x: graph.mf_matrix, y: y_one_hot})                
#                grad_stack = tf.convert_to_tensor(grads_stack)
#                print(cost_)
#                print(grads_stack)
                cnt = 0
                sess.run(zero_ops)

#                grads_stack = 0
#            print (grad_stack)
                
                
                
#                
                
#                for i in range(input_cons.node_features):
#                    gradi_list[i] = gradi[i][0]
#                gradi_sum += gradi_list
#            print(gradi)
#            sess.run(optimizer.apply_gradients(gradi_sum))                                      

#                _, loss = sess.run([opt, cost], feed_dict=InputList)
#                print(loss)
#            node_fun.append((candidate, fun))
#        if (graph.node_check(node_fun) & graph.link_check(node_fun)):
            # apply gradients
#            pass
            #calculate reward
#            graph.batch_function_placement(ser=s,
#                                           node_fun=node_fun)
                
#        y_RL1 = sess.run(y_predicted1, feed_dict={x: mf.mf_matrix})
#       
#        y_one_hot = y_one_hot.reshape(1, -1)
        
#    for epoch in range(input_cons.epoch_num):
        
#    print(y_RL)
#        InputList = {x: m_f,
#                     y: }
#        _, loss = sess.run([optimizer, cost], feed_dict=InputList)
#        trainLoss += loss
#        trainPredicted = sess.run(yHat, feed_dict={x: dataTrain})
#        trainPredicted = np.argmax(trainPredicted, 1) + 1
#        trainErrList.append(trainLoss)
#        trainAccList.append(acc(targetTrain, trainPredicted))
#        print("lass:", epoch, trainLoss)
#        print("Train Acc", trainAccList[epoch])
#        testPredicted = sess.run(yHat, feed_dict={x: dataTest})
#        testPredicted = np.argmax(testPredicted, 1) + 1
#        testErrList.append(sess.run(cost, feed_dict={x: dataTest, yTrue: targetTestModifid}))
#        testAccList.append(acc(targetTest, testPredicted))
#        print("Test Acc", testAccList[epoch])
#    w1, b1, w2, b2, w3, b3, wO, bO = sess.run([wLayer1, bLayer1, wLayer2,
#                                               bLayer2, wLayer3, bLayer3, wLayerOut, bLayerOut])
#        
##print(graph.start_file_line)
#
##print (IndentationError.read_path)
##Mf_cal()
#            
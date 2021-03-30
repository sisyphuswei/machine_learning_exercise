# -*- coding: utf-8 -*-
'''
Author: Xiaoqi Wei
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def read_dataset(feature_file, label_file):
    ''' Read data set in *.csv to data frame in Pandas'''
    df_X = pd.read_csv(feature_file)
    df_y = pd.read_csv(label_file)
    X = df_X.values # convert values in dataframe to numpy array (features)
    y = df_y.values # convert values in dataframe to numpy array (label)
    return X, y


def normalize_features(X_train, X_test):
    from sklearn.preprocessing import StandardScaler #import libaray
    scaler = StandardScaler() # call an object function
    scaler.fit(X_train) # calculate mean, std in X_train
    X_train_norm = scaler.transform(X_train) # apply normalization on X_train
    X_test_norm = scaler.transform(X_test) # we use the same normalization on X_test
    return X_train_norm, X_test_norm


def one_hot_encoder(y_train, y_test):
    ''' convert label to a vector under one-hot-code fashion '''
    from sklearn import preprocessing
    lb = preprocessing.LabelBinarizer()
    lb.fit(y_train)
    y_train_ohe = lb.transform(y_train)
    y_test_ohe = lb.transform(y_test)
    return y_train_ohe, y_test_ohe


class onelayer_NN:
    def __init__(self, X, y, hidden_layer_nn_1=100, hidden_layer_nn_2=100, lr=0.01):
        self.X = X # features
        self.y = y # labels (targets) in one-hot-encoder
        self.lr = lr # learning rate
        # Initialize weights
        self.nn = X.shape[1] # number of neurons in the input layer

        #self.hidden_layer_nn_1 = hidden_layer_nn_1 # number of neuron in the hidden layer
        # In this example, we only consider 1 hidden layer

        self.W1 = np.random.randn(self.nn, hidden_layer_nn_1) / np.sqrt(self.nn)
        self.b1 = np.zeros((1, hidden_layer_nn_1)) # double parentheses
        
        self.W2 = np.random.randn(hidden_layer_nn_1, hidden_layer_nn_2) / np.sqrt(hidden_layer_nn_1)
        self.b2 = np.zeros((1, hidden_layer_nn_2)) # double parentheses
        
        self.output_layer_nn = y.shape[1]
        self.W3 = np.random.randn(hidden_layer_nn_2, self.output_layer_nn) / np.sqrt(hidden_layer_nn_2)
        self.b3 = np.zeros((1, self.output_layer_nn))      
        
    def feed_forward(self):
        # hidden layer
        ## z_1 = xW_1 + b_1
        self.z1 = np.dot(self.X, self.W1) + self.b1
        ## activation function :  f_1 = \tanh(z_1)
        self.f1 = np.tanh(self.z1)
        ## z_2 = f_1W_2 + b_2
        self.z2 = np.dot(self.f1, self.W2) + self.b2
        ## activation function :  f_2 = \tanh(z_2)
        self.f2 = np.tanh(self.z2)
        
        # output layer
        ## z_3 = f_2W_3 + b_3
        self.z3 = np.dot(self.f2, self.W3) + self.b3   
        #\hat{y} = softmax}(z_3)$
        self.y_hat = softmax(self.z3)
        
    def back_propagation(self):
        # $d_3 = \hat{y}-y$
        d3 = self.y_hat - self.y
        # d_2 = (1-f^2_2)*(\hat{y}-y)W_3^T
        d2 = (1-self.f2*self.f2)*(d3.dot((self.W3).T))
        d1 = (1-self.f1*self.f1)*(d2.dot((self.W2).T))
        
        # dL/dW3 = f_2^T d3
        dW3 = np.dot(self.f2.T, d3)
        # dL/db3 = d3.axis=0
        db3 = np.sum(d3, axis=0, keepdims=True)
        
        # dL/dW2 = f_1^T d_2
        dW2 = np.dot(self.f1.T, d2)
        # dL/b_2 = d_2.axis=0
        db2 = np.sum(d2, axis=0, keepdims=True)
        # axis =0 : sum along the vertical axis

        # dL/dW_1} = x^T d_1
        dW1 = np.dot((self.X).T, d1)
        # dL/db_1 = d_1.axis=0
        db1 = np.sum(d1, axis=0, keepdims=True)
        
        # Update the gradident descent
        self.W1 = self.W1 - self.lr * dW1
        self.b1 = self.b1 - self.lr * db1
        self.W2 = self.W2 - self.lr * dW2
        self.b2 = self.b2 - self.lr * db2
        self.W3 = self.W3 - self.lr * dW3
        self.b3 = self.b3 - self.lr * db3
        
    def cross_entropy_loss(self):
        #  $L = -\sum_n\sum_{i\in C} y_{n, i}\log(\hat{y}_{n, i})$
        # calculate y_hat
        self.feed_forward()
        self.loss = -np.sum(self.y*np.log(self.y_hat + 1e-6))
        
    def predict(self, X_test):
        # Use feed forward to calculat y_hat_test
        # hidden layer
        ## z_1 = xW_1 + b_1
        z1 = np.dot(X_test, self.W1) + self.b1
        ## activation function :  f_1 = \tanh(z_1)
        f1 = np.tanh(z1)
        ## z_2 = f_1W_2 + b_2
        z2 = np.dot(f1, self.W2) + self.b2
        f2 = np.tanh(z2)
        # output layer
        ## z_3 = f_2W_3 + b_3
        z3 = np.dot(f2, self.W3) + self.b3    
        #\hat{y} = softmax}(z_2)$
        y_hat_test = softmax(z3)
        # the rest is similar to the logistic regression
        labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        num_test_samples = X_test.shape[0]
        # find which index gives us the highest probability
        ypred = np.zeros(num_test_samples, dtype=int) 
        for i in range(num_test_samples):
            ypred[i] = labels[np.argmax(y_hat_test[i,:])]
        return ypred
        
def softmax(z):
    exp_value = np.exp(z-np.amax(z, axis=1, keepdims=True)) # for stablility
    # keepdims = True means that the output's dimension is the same as of z
    softmax_scores = exp_value / np.sum(exp_value, axis=1, keepdims=True)
    return softmax_scores

def accuracy(ypred, yexact):
    p = np.array(ypred == yexact, dtype = int)
    return np.sum(p)/float(len(yexact))
        
# main
X_train, y_train = read_dataset('MNIST_X_train.csv', 'MNIST_y_train.csv')
X_test, y_test = read_dataset('MNIST_X_test.csv', 'MNIST_y_test.csv')

#print(X_train.shape)
#print(X_test.shape)

X_train_norm, X_test_norm = normalize_features(X_train, X_test)
y_train_ohe, y_test_ohe = one_hot_encoder(y_train, y_test)
# 
myNN = onelayer_NN(X_train_norm, y_train_ohe, hidden_layer_nn_1=300, hidden_layer_nn_2=100, lr=0.001)  
epoch_num = 200
for i in range(epoch_num):
    myNN.feed_forward()
    myNN.back_propagation()
    myNN.cross_entropy_loss()
    if ((i+1)%20 == 0):
        print('epoch = %d, current loss = %.5f' % (i+1, myNN.loss))         
        
y_pred = myNN.predict(X_test_norm)
print('Accuracy of our model ', accuracy(y_pred, y_test.ravel()))
# -*- coding: utf-8 -*-

'''
GPU command:
    THEANO_FLAGS=mode=FAST_RUN,device=gpu1,floatX=float32 python -B sentiment_lstm.py
'''

from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility
import os
import csv
from keras.callbacks import ModelCheckpoint
from keras.callbacks import Callback
from keras.callbacks import History
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.utils.np_utils import to_categorical


#def build_lstm(fold_number, train=None, val=None, test=None, aspect_name=None, path=None, aspect_number=0, binary=True):
def build_lstm(X_train, y_train, X_val, y_val): #, X_test, y_test):

    nb_rows, nb_feats = X_train.shape
    batch_size   = 64
    n_classes = 9
    nb_epoch = 20
    nb_hidden_layers = 64

    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)
    #y_test  = to_categorical(y_test)

    print('Build model...')
    model = Sequential()
    model.add(Embedding(nb_rows, nb_hidden_layers, input_length=nb_feats))
    model.add(Dropout(0.5))
    model.add(LSTM(nb_hidden_layers))  # try using a GRU instead, for fun
    model.add(Dropout(0.5))
    model.add(Dense(n_classes))
    model.add(Activation('sigmoid'))

    # try using different optimizers and different optimizer configs
    model.compile(
                  loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy']
                  # class_mode='binary'              
                  )

    checkpointer = ModelCheckpoint(filepath="/home/roger/weights.hdf5", verbose=1, save_best_only=True)
    acc_loss_monitor = History() 
    
    print('Train...')
    model.fit(X_train, y_train)#, batch_size=batch_size, nb_epoch=nb_epoch,
    #          validation_data=(X_val, y_val), callbacks=[checkpointer, acc_loss_monitor])#shuffle=True)
    
    val_accs = acc_loss_monitor.history['val_acc']
    val_loss = acc_loss_monitor.history['val_loss']
    
    model.load_weights('/home/roger/weights.hdf5')
    # model.save('models/model_fold_' + fold + '.h5')

    #score, test_acc = model.evaluate(X_test, y_test,
    #                            batch_size=batch_size)

    #print('Test score:', score)
    #print('Test accuracy:', test_acc)
    #
    #return test_acc, val_accs, val_loss

if __name__ == "__main__":
    X_train = []
    y_train = []
    print('Loading training data...')
    with open('/home/roger/Desktop/GoogleFeats/train_small.txt') as fin:
        for n, line in enumerate(fin):
            arr = line.strip().split()
            path, y, feat = arr[0], arr[1], arr[2:]
            feat = map(float, feat)
            y = int(y)
            X_train.append(feat)
            y_train.append(y)
            if n == 640:
                break
        X_train = np.array(X_train)
        y_train = np.array(y_train)

    X_val = []
    y_val = []
    print('Loading validation data...')
    with open('/home/roger/Desktop/GoogleFeats/val_feats.txt') as fin:
        for n, line in enumerate(fin):
            arr = line.strip().split()
            path, y, feat = arr[0], arr[1], arr[2:]
            feat = map(float, feat)
            y = int(y)
            X_val.append(feat)
            y_val.append(y)
            if n == 640:
                break
        X_val = np.array(X_val)
        y_val = np.array(y_val)

    X_test = []
    y_test = []
    #print('Loading testing data...')
    #with open('/home/roger/GoogleFeats/test_feats.txt') as fin:
    #    for line in fin:
    #        arr = line.strip().split()
    #        path, y, feat = arr[0], arr[1], arr[2:]
    #        feat = map(float, feat)
    #        y = int(y)
    #        X_test.append(feat)
    #        y_test.append(y)
    #    X_test = np.array(X_test)
    #    y_test = np.array(y_test)
    
    print('Building LSTM...')    
    build_lstm(X_train, y_train, X_val, y_val)#, X_test, y_test)

    

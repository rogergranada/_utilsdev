# -*- coding: utf-8 -*-

'''Train a LSTM on the IMDB sentiment classification task.

The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF+LogReg.

Notes:

- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.

- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.

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
from keras.models import Sequential, Model
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Input
#from keras.layers.embeddings import Embedding
from keras.layers.wrappers import TimeDistributed
from keras.layers.recurrent import LSTM
from keras.utils.np_utils import to_categorical

from os.path import realpath

BATCH_SIZE=64
NB_CLASSES=9
NB_EPOCHS=10
NB_HIDDEN=256

def main_lstm():
    main_input = Input(shape=(240000, 16, 1), name='main_input')
    vision_model = Sequential()
    vision_model.add(Convolution1D(16, 1, activation='relu', border_mode='same', input_shape=(16, 1)))
    vision_model.add(MaxPooling1D(2, 2))
    vision_model.add(Convolution1D(16, 16, activation='relu', border_mode='same'))
    vision_model.add(MaxPooling1D(2, 2))
    vision_model.add(Convolution1D(8, 32, activation='relu', border_mode='same'))
    vision_model.add(MaxPooling1D(2, 2))
    vision_model.add(Convolution1D(4, 64, activation='relu', border_mode='same'))
    vision_model.add(MaxPooling1D(2, 2))
    vision_model.add(Flatten())

    sec_input = TimeDistributed(vision_model)(main_input)
    x = LSTM(output_dim=512, return_sequences=True)(sec_input)
    x = LSTM(output_dim=64)(x)
    main_loss = Dense(1, activation='sigmoid', name='main_output')(x)
    model = Model(input=sec_input, output=main_loss)
    model.compile(optimizer='rmsprop', loss='mse')
    print(model.summary())

def load_vector_npy(inputfile):
    Xy = np.load(inputfile)
    X = Xy[:,:-1]
    y = Xy[:,-1]
    return X, y

def new_model():
    """Try this: https://github.com/fchollet/keras/issues/1641"""
    X_train, y_train = load_vector_npy('/home/roger/matrix.npy')
    X_test = X_train.copy()
    y_test = to_categorical(y_train, 9)
    y_train = to_categorical(y_train, 9)
    nb_samples, nb_feats = X_train.shape

    batch_size = 32

    print('Loading data...')
    #(X_train, y_train), (X_test, y_test) = t.LoadData()
    #print(len(X_train), 'train sequences')
    #print(len(X_test), 'test sequences')

    X_train = np.reshape(X_train, X_train.shape + (1,))
    X_test = np.reshape(X_test, X_test.shape + (1,))

    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    print('Build model...')
    model = Sequential()
    model.add(LSTM(1, input_shape=X_train.shape[1:]))

    model.compile(loss='mse',
                  optimizer='sgd',
                  class_mode="categorical")

    print("Train...")
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=3,
              validation_data=(X_test, y_test), show_accuracy=True)
    score, acc = model.evaluate(X_test, y_test,
                                batch_size=batch_size,
                                show_accuracy=True)
    print('Test score:', score)
    print('Test accuracy:', acc)

def build_lstm(X_train, y_train, X_test, y_test):
    nb_rows, nb_feats = X_train.shape

    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)
    #y_test  = to_categorical(y_test)
    #print(y_train[-1])

    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(256, input_dim=nb_rows))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, nb_epoch=100, batch_size=1, verbose=2)

    """
    Input(shape=(len(nb_rows),), dtype='int32')
    x = Input(shape=(nb_rows, nb_feats, 1))
    encoded_rows = TimeDistributed(LSTM(output_dim=16))(x)

    # Encodes columns of encoded rows.
    encoded_columns = LSTM(64)(encoded_rows)

    # Final predictions and model.
    prediction = Dense(nb_classes, activation='softmax')(encoded_columns)
    model = Model(input=x, output=prediction)
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # Training.
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epochs,
              verbose=1, validation_data=(X_val, y_val))

    # Evaluation.
    scores = model.evaluate(X_val, y_val, verbose=0)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])

    print('Build model...')
    model = Sequential()
    #model.add(Embedding(nb_rows, nb_hidden_layers, input_length=nb_feats))
    #model.add(Dropout(0.5))
    #model.add(LSTM(nb_hidden_layers, input_length=16))  # try using a GRU instead, for fun
    #model.add(Dropout(0.5))
    #model.add(Dense(n_classes))
    #model.add(Activation('sigmoid'))

    ## output_dim, init='glorot_uniform', inner_init='orthogonal', forget_bias_init='one', activation='tanh', 
    ## inner_activation='hard_sigmoid', W_regularizer=None, U_regularizer=None, b_regularizer=None, dropout_W=0.0, dropout_U=0.0
    model.add(LSTM(output_dim=nb_hidden_layers, init='uniform', inner_init='uniform', forget_bias_init='one', return_sequences=True, 
                   activation='tanh', inner_activation='sigmoid', input_shape=(nb_rows,nb_feats)))

    model.add(Dense(n_classes, activation='sigmoid'))
    #model.add(TimeDistributed(Dense(n_classes, activation='sigmoid')))
    ## sgd = SGD(lr = 0.1, decay = 1e-5, momentum=0.9, nesterov=True)
    ## model.compile(loss='mean_absolute_error', optimizer=sgd, metrics=['accuracy'])

    # try using different optimizers and different optimizer configs
    model.compile(
                  loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy']
                  # class_mode='binary'              
                  )

    #checkpointer = ModelCheckpoint(filepath="/home/roger/GoogleFeats/weights.hdf5", verbose=1, save_best_only=True)
    #acc_loss_monitor = History() 
    
    print('Train...')
    print(X_train.shape)
    print(y_train.shape)
    print(X_val.shape)
    print(y_val.shape)
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, validation_data=(X_val, y_val))
    #model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch,
    #          validation_data=(X_val, y_val), callbacks=[checkpointer, acc_loss_monitor])#shuffle=True)
    
    #val_accs = acc_loss_monitor.history['val_acc']
    #val_loss = acc_loss_monitor.history['val_loss']
    
    #model.load_weights('/home/roger/GoogleFeats/weights.hdf5')
    # model.save('models/model_fold_' + fold + '.h5')

    #score, test_acc = model.evaluate(X_test, y_test,
    #                            batch_size=batch_size)

    #print('Test score:', score)
    #print('Test accuracy:', test_acc)
    #
    #return test_acc, val_accs, val_loss
    """


def create_matrix(inputfile, frames=16):
    X, y = [], []
    print('Loading data from %s' % inputfile)
    with open(inputfile) as fin:
        for n, line in enumerate(fin):
            arr = line.strip().split()
            path, lbl, feat = arr[0], arr[1], arr[2:]
            feat = map(float, feat)
            lbl = int(lbl)
            X.append(feat)
            y.append(lbl)
    y = np.array(y, dtype=int)
    y = np.reshape(y, (len(y), 1))
    X = np.array(X)
    X = np.append(X, y, axis=1)
    return X


def unfold_matrix(inputfile):
    print('Loading data from: %s' % inputfile)
    Xy3D = np.load(inputfile)
    X = Xy3D[:,:-1]
    y = Xy3D[:,-1]
    return X, y


def create_matrix_split(inputfile, frames=16):
    X, y = [], []
    print('Loading data from %s' % inputfile)
    with open(inputfile) as fin:
        for n, line in enumerate(fin):
            arr = line.strip().split()
            path, lbl, feat = arr[0], arr[1], arr[2:]
            feat = map(float, feat)
            lbl = int(lbl)
            X.append(feat)
            y.append(lbl)
    y = np.array(y, dtype=int)
    y = np.reshape(y, (len(y), 1))
    X = np.array(X)
    X = np.append(X, y, axis=1)

    nb_rows, nb_cols = X.shape
    addframes = frames - (nb_rows % frames)
    for i in range(addframes):
        X = np.vstack([X, X[-1]])
    nb_dims = X.shape[0] / frames
    print('Reshaping matrix to (%d, %d, %d)' % (nb_dims, frames, nb_cols))
    X = X.reshape((nb_dims, frames, nb_cols))
    return X


def unfold_matrix_split(inputfile):
    print('Loading data from: %s' % inputfile)
    Xy3D = np.load(inputfile)
    X = Xy3D[:,:,:-1]
    y = Xy3D[:,:,-1]
    nb_dims, nb_rows, nb_cols = X.shape
    return X, y

if __name__ == "__main__":
    new_model()
    """
    if False:
        Xy = create_matrix('/home/roger/GoogleFeats/train_small.txt', frames=16)
        np.save('/home/roger/GoogleFeats/X_train.npy', Xy)
        Xy = create_matrix('/home/roger/GoogleFeats/val_feats.txt', frames=16)
        np.save('/home/roger/GoogleFeats/X_val.npy', Xy)
        #Xy = create_matrix('/home/roger/GoogleFeats/test_feats.txt', frames=16)
        #np.save('/home/roger/GoogleFeats/X_test3D.npy', Xy)
    else:
        X_train, y_train = unfold_matrix('/home/roger/GoogleFeats/X_train.npy')
        X_val, y_val = unfold_matrix('/home/roger/GoogleFeats/X_val.npy')
        #X_test, y_test = unfold_matrix('/home/roger/GoogleFeats/X_test3D.npy')
        print('Shape training:', X_train.shape, y_train.shape)
        print('Shape validation:', X_val.shape, y_val.shape)

        print('Building LSTM...')    
        build_lstm(X_train, y_train, X_val, y_val)#, X_test, y_test)
    """

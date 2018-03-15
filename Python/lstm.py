'''
    This example demonstrates an LSTM model 
    for text classification.
'''
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Reshape
from keras.layers.embeddings import Embedding
from keras.layers.wrappers import TimeDistributed
from keras.layers.recurrent import LSTM, GRU
from keras.optimizers import SGD, Adam
import numpy as np
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, History
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics

def create_matrix(inputfile, nb_classes=9, frames=32, stride=16, from_model=False, save_as=None):
    X, y = [], []
    print('Loading data from %s' % inputfile)
    if from_model:
        X = np.load('/home/roger/X_'+save_as+'.npy')
        y = np.load('/home/roger/y_'+save_as+'.npy')
    else:
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
        y = np_utils.to_categorical(y, nb_classes)
        X = np.array(X)
        #X = np.append(X, y, axis=1)

        #normalize values
        #scaler = MinMaxScaler(feature_range=(0, 1))
        #X = scaler.fit_transform(X)

        # fill missing rows
        nb_rows, nb_cols = X.shape
        addframes = stride - ((nb_rows - frames) % stride)
        print 'Adding : ', addframes
        for i in range(addframes):
            X = np.vstack([X, X[-1]])
            y = np.vstack([y, y[-1]])
            
        print 'Modified shape X: ', X.shape
        print 'Modified shape y: ', y.shape

        print('building matrix...')
        nb_rows, nb_cols = X.shape
        nb_dims = 1 + ((nb_rows - frames) / stride)
        print 'Divide into dimensions: ', nb_dims
        X_total = []
        y_total = []
        index = 0
        for dim in xrange(nb_dims):
            final = index + frames
            X_total.append(X[index:final])
            y_total.append(y[index:final])
            index = index + stride

        X = np.array(X_total)
        y = np.array(y_total)

        if save_as:        
            np.save('/home/roger/X_'+save_as+'.npy', X)
            np.save('/home/roger/y_'+save_as+'.npy', y)
    return X, y


print("Loading data...")
#X_train, y_train = create_matrix('/home/roger/GoogleFeats/train_feats.txt', nb_classes=9, frames=16, stride=8, from_model=False, save_as='train')
#X_test, y_test = create_matrix('/home/roger/GoogleFeats/val_feats.txt', nb_classes=9, frames=16, stride=8, from_model=False, save_as='val')

X_train, y_train = create_matrix('/home/roger/AlexnetFeats/feats_train.txt', nb_classes=9, frames=32, stride=32, from_model=False, save_as='train')
X_test, y_test = create_matrix('/home/roger/GoogleFeats/feats_val.txt', nb_classes=9, frames=32, stride=32, from_model=False, save_as='val')

print X_train.shape
print('Building model...')
INPUT_LEN = 16
INPUT_DIM = 1024
OUTPUT_LEN = 9

model = Sequential()
model.add(LSTM(512, return_sequences=True, input_dim=INPUT_DIM, input_length=INPUT_LEN))
model.add(Dropout(0.5))
#model.add(LSTM(512, return_sequences=True))
#model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(OUTPUT_LEN)))
model.add(Activation('softmax'))

sgd = Adam(lr=1e-5)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#checkpointer = ModelCheckpoint(filepath='weights.{epoch:02d}-{val_loss:.2f}.hdf5', verbose=1, save_best_only=True)
#acc_loss_monitor = History()

model.fit(X_train, y_train, batch_size=32, nb_epoch=20, validation_data=(X_test, y_test)) #, callbacks=[checkpointer, acc_loss_monitor])
#model.save('/home/roger/lstm.h5')

#val_accs = acc_loss_monitor.history['val_acc']
#print 'Validation accuracy:', val_accs


# test phase
#score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=1, show_accuracy=True)
#print('Test score:', score[0])
#print('Test accuracy:', score[1])
#
#y_score = model.predict(X_test, batch_size=batch_size)
#auc_score = metrics.roc_auc_score(y_test, y_score)
#print("*** AUC for ROC = %0.3f\n" % auc_score)

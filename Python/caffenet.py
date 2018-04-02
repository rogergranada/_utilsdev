#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script parses the Caffe framework for external access.
"""
import sys
sys.path.insert(0, '../..')
import logging
logger = logging.getLogger('caffe.caffenet')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import sys
import re
import subprocess
import numpy as np
from os.path import splitext, join, realpath, isfile
import caffe
import pandas as pd
from google.protobuf import text_format
from caffe.proto import caffe_pb2

import prototxt
from classes import progressbar


class CaffeLoader(object):
    """
    Class to load main configuration of caffe
    """
    def __init__(self, inputfolder, gpu_id=0):
        """
        Load caffe and set variables
    
        Parameters:
        -----------
        inputfolder : string
            path to the folder containing the model file `deploy.prototxt`
            and the pre trained model `.caffemodel`
        layer : string
            layer name to extract the features
        gpu_id : int
            id of the GPU where the caffe model is processed. In case of negative
            number, CPU is used
        """
        if gpu_id < 0:
            caffe.set_mode_cpu()
        else:
            caffe.set_mode_gpu()
            #caffe.set_device(gpu_id)
        inputfolder = realpath(inputfolder)
        self.protofile, self.caffemodel = self._findFiles(inputfolder)
        self.mean = [128.,128.,128.]


    def _findFiles(self, inputfolder):
        """
        Find the caffe model and the trained model files in folder

        Parameters:
        -----------
        inputfolder : string
            path to the folder containing the model file `deploy.prototxt`
            and the pre trained model `.caffemodel`
        """
        protofile, caffemodel = None, None
        files = os.listdir(inputfolder)
        for f in files:
            name, ext = splitext(f)
            if ext == '.caffemodel':
                caffemodel = join(inputfolder, f)
            elif f == 'deploy.prototxt':
                protofile = join(inputfolder, f)
        return protofile, caffemodel


    def _getMean(self, mean):
        """
        Return the value of mean according to the type of `mean` the function
        receives

        Parameters:
        -----------
        mean : {str, array_like, npy}
            value of mean

        Notes:
        ------
        In case mean receives a string as input, select a default value according
        to the string. Values to str(mean) are: `rgb` and `hof`.
        In case mean receives a binary file or a array_like object, returns the 
        object itself.
        """
        if isinstance(mean, str):
            if mean == 'rgb':
                R, G, B = 126.408, 122.788, 132.129 
                return np.asarray([R, G, B])
            elif mean == 'hof':
                R, G, B = 10.757, 10.832, 10.758
                return np.asarray([R, G, B])
            elif mean == 'ycbcr':
                R, G, B = 132.058, 128.828, 122.513
                return np.asarray([B, R, G])
            elif isfile(mean) and mean.endswith('.npy'):
                return np.load(mean).mean(1).mean(1)
        elif isinstance(mean, list) and len(mean) == 3:
            return mean


    def setModel(self, model):
        """
        Set a specific caffemodel that is not in Proto folder
    
        Parameters:
        -----------
        model : string
            path to a caffemodel file containing the weights of the CNN
        """
        self.caffemodel = model


    def getShapes(self):
        """
        Return a panda frame with the shapes of all layers of the CNN.
        """
        shapes = pd.DataFrame(columns=('size', 'filters', 'width', 'height'))
        for layer, blob in self.net.blobs.iteritems():
            values = blob.data.shape
            if len(values) < 4:
                values = np.lib.pad(values, (0,4-len(values)), 'constant', constant_values=-1)
            shapes.loc[layer] = values
        return shapes


    def getNumberParams(self):
        """
        Return a panda frame with the number of paramenters for each layer.
        """
        params = pd.DataFrame(columns=('filters', 'depth', 'width', 'height', 'bias', 'total'))
        for layer, weights in self.net.params.iteritems():
            vec = []
            total = (np.product(weights[0].data.shape) + np.product(weights[1].data.shape))
            values = weights[0].data.shape
            if len(weights) < 4:
                values = np.lib.pad(values, (0,4-len(values)), 'constant', constant_values=-1)
            vec.extend(values)
            vec.extend(weights[1].data.shape)
            vec.append(total)
            params.loc[layer] = vec
        return params
#End of class CaffeLoad


class CaffeClassifier(CaffeLoader):
    """
    Class to load caffe and predict labels for input images
    """
    def __init__(self, inputfolder, gpu_id=0, mean='rgb', dims=224, model=None):
        """
        Load caffe and set variables
    
        Parameters:
        -----------
        inputfolder : string
            path to the folder containing the model file `deploy.prototxt`
            and the pre trained model `.caffemodel`
        gpu_id : int
            id of the GPU where the caffe model is processed
        mean : {str, array_like, npy}
            value of mean
        dims : int
            size of the input image
        model : string
            path to a caffemodel file containing the weights of the CNN
        """
        CaffeLoader.__init__(self, inputfolder, gpu_id=gpu_id)
        meanvalues = self._getMean(mean)

        logger.info('loading deploy.prototxt from %s' % inputfolder)
        logger.info('using mean for %s' % mean)

        if model:
            self.setModel(model)
        if self.caffemodel and self.protofile:
            self.net = caffe.Classifier(self.protofile, 
                                self.caffemodel,
                                mean=meanvalues,
                                channel_swap=(2,1,0),
                                raw_scale=256,
                                image_dims=(dims, dims)
                              )
        else:
            logger.error('Cannot find prototxt or caffemodel file')
            sys.exit(0) 
        self.prediction = None


    def predict(self, imgfile, N=9):
        topN = []
        caffeimg = caffe.io.load_image(imgfile)
        self.prediction = self.net.predict([caffeimg])
        preds = self.prediction.copy()[0]
        #print np.around(preds, decimals=2)
        for n in range(N):
            top = preds.argmax()
            val = preds[top]
            topN.append((top, val))
            preds[top] = -1.0
        return topN
#End of class CaffeClassifier


class CaffeFeatures(CaffeLoader):
    """
    Class to load caffe and extract features from images
    """
    def __init__(self, inputfolder, layer, gpu_id=0, mean='rgb', dims=256, model=None):
        """
        Load caffe and set variables
    
        Parameters:
        -----------
        inputfolder : string
            path to the folder containing the model file `deploy.prototxt`
            and the pre trained model `.caffemodel`
        layer : string
            layer name to extract the features
        gpu_id : int
            id of the GPU where the caffe model is processed
        mean : {str, array_like, npy}
            value of mean
        dims : int
            size of the input image
        model : string
            path to a caffemodel file containing the weights of the CNN
        """
        CaffeLoader.__init__(self, inputfolder, gpu_id=gpu_id)
        meanvalues = self._getMean(mean)
        logger.info('loading deploy.prototxt from %s' % inputfolder)
        if model:
            self.setModel(model)
        if self.caffemodel and self.protofile:
            self.net = caffe.Net(self.protofile, self.caffemodel, caffe.TEST)
            self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
            self.transformer.set_mean('data', meanvalues)
            self.transformer.set_transpose('data', (2,0,1))
            self.transformer.set_raw_scale('data', 256.0)
            self.net.blobs['data'].reshape(1,3, dims, dims)
            self.layer = layer        
        else:
            logger.error('Cannot find prototxt or caffemodel file')
            sys.exit(0) 


    def get_features(self, imgfile):
        """
        Extract features from file.

        Parameters:
        -----------
        imgfile : string
            path to the image to extract the features
        """
        if self.layer not in self.net.blobs:
            raise TypeError("Invalid layer name: " + self.layer)
        caffeimg = caffe.io.load_image(imgfile)
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', caffeimg)
        output = self.net.forward()
        return self.net.blobs[self.layer].data[0]
#End of class CaffeLayers


class CaffeShapes(CaffeLoader):
    """
    Class to load caffe and extract the shapes of the model
    """
    def __init__(self, inputfolder, gpu_id=0, model=None):
        """
        Load caffe and set variables
    
        Parameters:
        -----------
        inputfolder : string
            path to the folder containing the model file `deploy.prototxt`
            and the pre trained model `.caffemodel`
        gpu_id : int
            id of the GPU where the caffe model is processed
        model : string
            path to a caffemodel file containing the weights of the CNN
        """
        CaffeLoader.__init__(self, inputfolder, gpu_id=gpu_id)
        logger.info('loading deploy.prototxt from %s' % inputfolder)
        if model:
            self.setModel(model)
        if self.caffemodel and self.protofile:
            self.net = caffe.Net(self.protofile, caffe.TEST)
        else:
            logger.error('Cannot find prototxt or caffemodel file')
            sys.exit(0) 


    def print_shapes(self):
        """
        Print the shape of all layers of the CNN.
        """
        total_filter = 0
        for layer_name, blob in self.net.blobs.iteritems():
            ts = ''
            for x in blob.data.shape:
                ts += '%5i' % x
            print ts, ' ' * (25 - len(ts)), layer_name


    def print_weights(self):
        df = self.getNumberParams()
        print df
        print 'Total: ', df['total'].sum(axis=0)
#End of class CaffeShapes


class CaffeTest(object):
    """
    Use bash to run `caffe test` on `.caffemodel` files and extract all the accuracies
    """
    def __init__(self, model, weight, gpu=0, iterations=0):
        """
        Create command line to call `caffe test`
    
        Parameters:
        -----------
        model : string
            path to the `train_val.prototxt` file
        weight : string
            path to the `.caffemodel` file containing weights
        iterations : int
            number of iterations on test
        gpu : int
            GPU id
        net : string
            name of the network (googlenet, alexnet)
        """
        self.model = realpath(model)
        self.run = False
        self.nb_images = 0
        self.model_acc = None
        self.model_loss = None
        self.i = -1

        self.protofile = prototxt.TrainVal(self.model)
        self.net = self.protofile.netname()
        if iterations:
            self.iterations = iterations
        else:
            self.iterations = self._calculateIterations()

        logger.info('calling: caffe test -model %s -weights %s -gpu %d -iterations %d' % (model, weight, gpu, self.iterations))
        self.comm = 'caffe test -model '+model+' -weights '+weight+' -gpu '+str(gpu)+' -iterations '+str(self.iterations)


    def __iter__(self):
        """
        Iterate through all test and yield each line
        """
        p = subprocess.Popen(self.comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            line = p.stdout.readline()
            if not line:
		        break
            line = line.strip()
            yield line


    def _run(self):
        """
        Run the test checking accuracy and loss
        """
        pb = progressbar.ProgressBar(self.iterations)
        p = subprocess.Popen(self.comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            line = p.stdout.readline()
            if not line:
		        break
            line = line.strip()
            acc = self._checkAccuracy(line)
            if acc:
                self.model_acc = acc
            loss = self._checkLoss(line)
            if loss:
                self.model_loss = loss

            if self._checkUpdate(line):
                pb.update()
        self.run = True

    """
    def _loadParametersFromPrototxt(self):
        
        Extract the number of images from `train_val.txt`, the batch size and
        the network name 
        
        net = caffe_pb2.NetParameter()
        text_format.Merge(open(self.model).read(), net)
        self.net = net.name.lower()
        for n in range(len(net.layer)):
            if net.layer[n].name == 'data' and net.layer[n].include[0].phase == 1:
                path_images = net.layer[n].image_data_param.source
                self.batchsize = net.layer[n].image_data_param.batch_size
                break
        self.nb_images = len(open(path_images).readlines())
    """

    def _calculateIterations(self):
        """
        Calculate the number of iterations based on batch size and number of images
        """
        #iterations = self.nb_images/self.batchsize
        imgs = self.protofile.nb_test()
        batch = self.protofile.batch_test()
        iterations = imgs/batch
        if imgs % batch != 0:
            iterations += 1
        return iterations


    def _checkUpdate(self, line):
        """
        Check if should update the progress bar
        """
        has_bash = re.findall("308] Batch \d+", line)
        if has_bash:
            nb_bash = int((has_bash[0]).split()[-1])
            if nb_bash != self.i:
                self.i = nb_bash
                return True
        return False


    def accuracy(self):
        """
        Call the Caffe test and get the average accuracy for the model
        """
        if not self.run:
            self._run()
        return self.model_acc


    def loss(self):
        """
        Call the Caffe test and get the average loss for the model
        """
        if not self.run:
            self._run()
        return self.model_loss            


    def _checkAccuracy(self, line):
        """
        Extract the accuracy value from line
        """
        has_acc = False
        acc_layer = self.protofile.layer_accuracy()
        #print acc_layer, line
        has_acc = re.findall('325] '+acc_layer+' = \d+[\.]?\d*', line)
        if has_acc:
            return float((has_acc[0]).split()[-1])
        return None


    def _checkLoss(self, line):
        """
        Extract the loss value from line
        """
        has_loss = False
        if self.net == 'alexnet':
            has_loss = re.findall("325] loss = \d+[\.]?\d*", line)
        elif self.net == 'googlenet':
            has_loss = re.findall("313] Loss: \d+[\.]?\d*", line)
        if has_loss:
            return float((has_loss[0]).split()[-1])
        return None
#End of class CaffeTest


def weight_files(dirin):
    """
    Return a list containing all models inside the folder

    Parameters:
    -----------
    dirin : string
        path to the folder containing `.caffemodel` files
    """
    listfiles = os.listdir(dirin)
    models = []
    for fname in sorted(listfiles):
        if fname.endswith('.caffemodel'):
            models.append(join(dirin, fname))
    return models

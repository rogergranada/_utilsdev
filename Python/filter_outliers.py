#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import matplotlib as mpl
# Force matplotlib to not use any Xwindows backend.
mpl.use('Agg')
import operator
from os.path import join
from progressBar import ProgressBar
from collections import Counter
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

from plotSequence import Labels
from pathfile import PathFile


PATH='/usr/share/datasets/Trainman/Kitchen/Data/'



def loadFile(inputfile):
    """
    Receive a file containing the path, true label and predicted
    label and return a list for each element.

    Parameters:
    -----------
    inputfile : string
        path to the file containing the data

    Returns:
    --------
    n : int
        number of lines of the file
    lpath : array_like
        list containing the paths as they appear in the file
    ly : array_like
        list containing the true labels as they appear in the file
    lpred : array_like
        list containing the predicted labels as they appear in the file
    """
    lpath, ly, lpred = [], [], []
    with open(inputfile) as fin:
        for n, line in enumerate(fin):
            path, y, pred = line.strip().split()
            lpath.append(path)
            ly.append(int(y))
            lpred.append(int(pred))
    return (n+1, lpath, ly, lpred) 


def loadDictionaryFromFile(inputfile):
    """
    Generate a dictionary in the form:
        {id_data: {activity: {image: (y, pred)}}}
        dic [0]['boild-egg'][0] = (0, 0)
    from a file containing paths and labels as:
        /usr/share/datasets/Trainman/Kitchen/Data/data1/boild-egg/img256/0.jpg 0 0

    Parameters:
    -----------
    inputfile : string
        file containing paths and labels
    """
    dic = {}
    with open(inputfile) as fin:
        for n, line in enumerate(fin):
            path, y, pred = line.strip().split()
            path = path.replace(PATH, '')
            arr = path.split('/')
            id_data = int((arr[0])[-1])
            activity = arr[1]
            id_img = int(arr[-1].replace('.jpg', ''))
            y = int(y)
            pred = int(pred)
            if dic.has_key(id_data):
                if dic[id_data].has_key(activity):
                    dic[id_data][activity][id_img] = (y, pred)
                else:
                    dic[id_data][activity] = {id_img: (y, pred)}
            else:
                dic[id_data] = {activity: {id_img: (y, pred)}}
    return dic, n+1







def saveNewFrames(fname, paths, y, pred):
    with open(fname, 'w') as fout:
        for i in xrange(len(y)):
            fout.write('%s %d %d\n' % (paths[i], y[i], pred[i]))


def filterOutliers(inputfile, window=236):
    """

    Parameters:
    -----------
    inputfile : string
        file containing paths, labels and predictions
    """


    f = Filter(preds, window)
    newp = []
    for target, lwin in f:
        dc = Counter(lwin)
        target = max(dc.iteritems(), key=operator.itemgetter(1))[0]
        newp.append(target)

    #saveNewFrames('newframes.txt', paths, ys, newp)

    sequence = []
    actual = 0
    counter = 0
    for p in preds:
        if p == actual:
            counter += 1
        else:
            sequence.append((actual, counter))
            counter = 0
            actual = p

    #print sequence 
    mintuple = None
    minval = float('inf')
    for id, valse in sequence:
        if valse < minval:
            minval = valse
            mintuple = (id, valse)
    print 'Minimum:',mintuple
    lab = Labels(ys, newp)
    #lab = Labels(ys, preds)
    lab.plotFrameSequence('frameseq2x.png')
    lab.plotAllBars('allbars_2x.png')


def searchForBest(inputfile, tries=100, step=2):
    paths, ys, preds = [], [], []
    with open(inputfile) as fin:
        for n, line in enumerate(fin):
            path, y, pred = line.strip().split()
            paths.append(path)
            ys.append(y)
            preds.append(pred)

    pb = ProgressBar(len(range(1, tries, step)))
    accs = [calculateAccuracy(ys, preds)]
    x = [0]
    bestwindow = 0
    bestacc = 0.0
    for window in xrange(1, tries, step):
        f = Filter(preds, window)
        newp = []
        for target, lwin in f:
            dc = Counter(lwin)
            target = max(dc.iteritems(), key=operator.itemgetter(1))[0]
            newp.append(target)

        accuracy = calculateAccuracy(ys, newp)
        accs.append(accuracy)
        if accuracy > bestacc:
            bestacc = accuracy
            bestwindow = window
        pb.update()
    x.extend(range(1,tries,step))
    #print len(x), len(accs)
    plt.plot(x, accs)
    plt.savefig('accur.png', bbox_inches='tight')
    print
    print 'Best window:', bestwindow
    print 'Best accuracy:', bestacc
    return bestwindow


def filterOutliersFromWindow(y, pred, window=236):
    """

    Parameters:
    -----------
    """
    f = Filter(pred, window)
    newp = []
    for target, lwin in f:
        #dc = Counter(lwin)
        #target = max(dc.iteritems(), key=operator.itemgetter(1))[0]
        #target = (stats.mode(np.array(lwin)))[0][0]
        target = np.bincount(lwin).argmax()
        newp.append(target)

    #saveNewFrames('newframes.txt', paths, ys, newp)

    sequence = []
    actual = 0
    counter = 0
    for p in pred:
        if p == actual:
            counter += 1
        else:
            sequence.append((actual, counter))
            counter = 0
            actual = p

    #print sequence 
    mintuple = None
    minval = float('inf')
    for id, valse in sequence:
        if valse < minval:
            minval = valse
            mintuple = (id, valse)
    print 'Minimum:',mintuple
    lab = Labels(y, pred)
    #lab = Labels(ys, preds)
    lab.plotFrameSequence('frameseqLocalOrig.png')
    lab.plotAllBars('allbarsLocalOrig.png')



def searchForBestAccuracy(y, pred, tries=100, step=1):
    pb = ProgressBar(len(range(1, tries, step)))
    accs = [calculateAccuracy(y, pred)]
    x = [0]
    bestwindow = 0
    bestacc = 0.0
    for window in xrange(1, tries, step):
        f = Filter(pred, window)
        newp = []
        for target, lwin in f:
            dc = Counter(lwin)
            target = max(dc.iteritems(), key=operator.itemgetter(1))[0]
            newp.append(target)

        accuracy = calculateAccuracy(y, newp)
        accs.append(accuracy)
        if accuracy > bestacc:
            bestacc = accuracy
            bestwindow = window
        pb.update()
    x.extend(range(1,tries,step))
    #print len(x), len(accs)
    plt.plot(x, accs)
    plt.savefig('accurLocal.png', bbox_inches='tight')
    print
    print 'Best window:', bestwindow
    print 'Best accuracy:', bestacc
    return bestwindow

def verifyFramesForAction(inputfile):
    dic, n = dictionaryFromPathfile(inputfile)
    print dic.keys()
    for data in sorted(dic):
        print dic[data].keys()
        for act in sorted(dic[data]):
            y, pred = [], []
            for img in sorted(dic[data][act]):
                y.append(dic[data][act][img][0])
                pred.append(dic[data][act][img][1])
            #searchForBestAccuracy(y, pred, tries=500, step=5)
            print data, act
            filterOutliersFromWindow(y, pred, window=290)
            break
        break
#############################################################################################################
def calculateAccuracy(y, pred):
    """
    Calculate the accuracy of the predicted labels when comparing
    with the true labels.

    Parameters:
    -----------
    y : array_like
        list containing the true labels
    pred : array_like
        list cotaining the predicted labels

    Returns:
    --------
    acc : float
        Accuracy of the predicted labels
    """
    correct = 0.0
    for ly, lp in zip(y, pred):
        if ly == lp:
            correct += 1.0
    if correct > 0:
        acc = float(correct)/len(y)
    else:
        acc = 0.0
    return acc


class Window(object):
    """
    Class that generates a slidly window from an array
    """ 
    def __init__(self, vec, size):
        """
        Initiates class Window

        Parameters:
        -----------
        vec : array_like
            list containing labels
        size : int
            size of the window
        """
        self.vec = vec
        self.size = (size-1)/2
        self.i = 0
        self.window = []
        

    def __iter__(self):
        """
        Iterates over the list of labels, yielding a window of
        size equals to `self.size` each time.

        Yields:
        -------
        i : int
            index of the original list
        vec[i] : {string, int}
            target label in the list at index `i`
        window : array_like
            list containing a subset of the elements of the 
            original list
        """
        for i in range(len(self.vec)):
            self.i = i
            self.window = []
            if i <= self.size:
                 self.window = self.vec[:i]
            elif i > self.size:
                 self.window.extend(self.vec[i-self.size:i])
            self.window.append(self.vec[i])
            if i >= (len(self.vec) - self.size):
                 self.window.extend(self.vec[i+1:])
            elif i < (len(self.vec) - self.size):
                 self.window.extend(self.vec[i+1:i+self.size+1])
            yield self.i, self.vec[i], self.window

    def __str__(self):
        return 'Window of size: %d with target %s [index %d]' % ((self.size+1)*2, self.vec[self.i], self.i)
# End of class Window


def seachBestWindowSize(inputfile, outputfile, maxsize=100, increment=1):
    """
    From a file contanining paths, true labels and predicted labels
    select the best window size (the one with the highest accuracy)
    to apply mode.

    Parameters:
    -----------
    inputfile : string
        path to the file containing paths, true labels and predicted labels
    outputfile : string
        path to the file where the stats are recorded
    tries : int
        maximum size of the window
    step : int
        number of elements in a window
    """
    pfile = PathFile(inputfile)
    #fout = open(outputfile, 'w')
    #pb = ProgressBar(pfile.N())
    i = 0
    for data, activity, y, pred in pfile:
        accs = [calculateAccuracy(y, pred)]
        x = [0]
        bestwindow = 0
        bestacc = 0.0
        
        for size in xrange(1, maxsize, increment):
            w = Window(pred, size)
            newpred = []

            for index, target, window in w:
                #dc = Counter(lwin)
                #target = max(dc.iteritems(), key=operator.itemgetter(1))[0]
                target = np.bincount(window).argmax()
                newpred.append(target)

            accuracy = calculateAccuracy(y, newpred)
            accs.append(accuracy)
            if accuracy > bestacc:
                bestacc = accuracy
                bestwindow = size
        i += 1
        x.extend(range(1,maxsize,increment))
        pb.update()
        #plt.clf()
        #plt.plot(x, accs)
        #print data, activity, bestacc, bestwindow
        #plt.savefig('sequences/'+str(data)+'-'+activity+'-acc.png', bbox_inches='tight')
        #fout.write('Cooker: %d\n\tActivity: %s\n\tAccuracy = %f\n\tWindow = %d\n' % 
        #          (data, activity, bestacc, bestwindow))
    #fout.close()


def verifyMinimum(sequence):
    """
    Verify which is the label that contains the minimum number of 
    occurrences in the sequence.

    Parameters:
    -----------
    sequence : array_like
        list containing labels and values where the values are the
        frequency of the label
    
    Returns:
    --------
    ymin : int
        label of the minimum value 
    minim : int
        minimal frequency of the list
    """
    minim = float('inf')
    ymin = None
    for y, val in sequence:
        if val < minim:
            minim = val
            ymin = y
    return (ymin, minim)


def verifySequenceOfActions(inputfile, mode='y'):
    """
    From a file containing paths, true labels and predicted labels
    identify the sequence of actions.

    Parameters:
    -----------
    inputfile : string
        path to the file containing the data
    mode : string {y, pred}
        the list that generates the sequence 
    """
    pfile = PathFile(inputfile)
    for data, activity, y, pred in pfile:
        #print 'Cooker:', data
        #print '\tActivity:', activity
        #print '\t\tFrames:', len(y)

        if mode == 'y':
            elements = y
        else:
            elements = pred

        actual = 0
        sequence = []
        counter = 0
        for p in elements:
            if p == actual:
                counter += 1
            else:
                sequence.append((actual, counter))
                counter = 1
                actual = p
        sequence.append((actual, counter))
        
        #minim = verifyMinimum(sequence)
        #print '\t\tMinimum: ', minim
        #if data == 7 and activity == 'ham-egg':
        #    for el, nbf in sequence:
        #        print el, nbf

        #plot = Labels(y, pred)
        #plot.plotFrameSequence('sequences/%d-%s.png' % (data, activity))
        break


if __name__ == "__main__":
    """
    Input file contains the format: `path_to_the_file true_label predicted_label`, as:

    /usr/share/datasets/Juarez_Kitchen_Dataset/Train/data1/boild-egg-1/image_res_256_jpg/0.jpg 0 0
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='the file received as input.')
    parser.add_argument('outputfile', metavar='file_output', help='the file received as output.')
    args = parser.parse_args()

    #verifySequenceOfActions(args.inputfile, mode='y')
    seachBestWindowSize(args.inputfile, args.outputfile, maxsize=500, increment=5)
    #bestw = searchForBest(args.inputfile, tries=100, step=1)
    #filterOutliers(args.inputfile, window=bestw)
    print

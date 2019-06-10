#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import re
from os.path import basename, splitext
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

def getEpochAccLoss(filein):
    """
    Read a file and return three lists containing the ids of the epochs,
    the accuracy and the loss of the models for each epoch.

    Parameters:
    -----------
    filein : string
        Input file containing the accuracy and the loss
    """
    ar_epochs = []        
    ar_acc = []
    ar_loss = []
    with open(filein) as fin:
        dic = {}
        for n, line in enumerate(fin):
            line = line.strip()
            if line.startswith('---'):
                dic[model] = {'acc': acc, 'loss': loss}
            else:
                if line.startswith('Model:'):
                    model = int(re.findall("\d+", line)[-1])
                elif line.startswith('Loss:'):
                    loss = re.findall("\d+[\.]?\d*", line)[-1]
                elif line.startswith('accuracy'):
                    acc = re.findall("\d+[\.]?\d*", line)[-1]

        for epoch, id_snap in enumerate(sorted(dic)):
            ar_epochs.append(epoch)
            ar_acc.append(dic[id_snap]['acc'])
            ar_loss.append(dic[id_snap]['loss'])
    return (ar_epochs, ar_acc, ar_loss)


def plotInSubplots(filein):
    """
    Plot values of accuracy and loss for models using two subplots

    Parameters:
    -----------
    filein : string
        Input file containing the accuracy and the loss
    """
    model, acc, loss = getEpochAccLoss(filein)
    fig = matplotlib.pyplot.figure()
    img1 = fig.add_subplot(2,1,1)
    img1.plot(model, acc, '-b')
    img1.set_ylabel('Accuracy')
    img2 = fig.add_subplot(2,1,2)
    img2.plot(model, loss, '-g')
    img2.set_xlabel('Epochs')
    img2.set_ylabel('Loss')
    filename = splitext(basename(filein))[0]
    matplotlib.pyplot.savefig(filename+'_2Plot.png')


def plotInOnePlot(filein):
    """
    Plot values of accuracy and loss for models in the same plot

    Parameters:
    -----------
    filein : string
        Input file containing the accuracy and the loss
    """
    model, acc, loss = getEpochAccLoss(filein)
    fig, ax1 = plt.subplots()
    ax1.plot(model, acc, '-b', label='Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(model, loss, '-r', label='Loss')
    ax2.set_ylabel('Loss', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    filename = splitext(basename(filein))[0]
    plt.savefig(filename+'_1Plot.png')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='the file received as input.')
    parser.add_argument('-p', '--plots', metavar='plots', type=int, 
                        help='numbert of subplots', default=1)
    args = parser.parse_args()

    if args.plots == 1:
        plotInOnePlot(args.inputfile)
    else:
        plotInSubplots(args.inputfile)

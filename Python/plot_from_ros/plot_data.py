#/usr/bin/env python

"""
Generate trajectories and distribution plots for boats.

NOTE: When generating plots for Overtake and HeadsOn, a
      manual range of values must be change in line 57-58. 
"""
import os
import argparse
import sys
import numpy as np
from os.path import exists, dirname, join, isdir, isfile

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from matplotlib import pyplot as plt
import pickle
import numpy as np

import filehandler as fh
from filehandler import Stats, Boat
from matplotlib import pylab

PARAMS = {'legend.fontsize': 28,
          'figure.figsize': (15, 10),
         'axes.labelsize': 28,
         'axes.titlesize':28,
         'xtick.labelsize': 28,
         'ytick.labelsize': 28}
pylab.rcParams.update(PARAMS)


def minimal_distance(boat1, boat2):
    lowest_distance = float('inf')
    for b1x, b1y, b2x, b2y in zip(boat1.x, boat1.y, boat2.x, boat2.y):
        dist = np.linalg.norm(np.array([b1x, b1y])-np.array([b2x, b2y]))
        if dist < lowest_distance:
            lowest_distance = dist
            min1x = b1x
            min1y = b1y
            min2x = b2x
            min2y = b2y
    return min1x, min1y, min2x, min2y


def plot_trajectories(boat1, boat2, fname, angle1=40, angle2=60):
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Most plots
    ax.set_xlim(398, 427)
    ax.set_ylim(103, 135)
    # Heads on and overtake
    # ax.set_xlim(445, 485)
    # ax.set_ylim(100, 115)

    ax.plot(boat1.x, boat1.y, '-b', label=boat1.name, linewidth=2)
    ax.plot(boat2.x, boat2.y, '-r', label=boat2.name, linewidth=2)

    min1x, min1y, min2x, min2y = minimal_distance(boat1, boat2)

    plt.scatter(min1x, min1y, s=200, marker=(3, 0, angle1))
    plt.scatter(min2x, min2y, s=200, marker=(3, 0, angle2))
    plt.xlabel('Coordenadas em metros')
    plt.ylabel('Coordenadas em metros')
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    plt.savefig(fname, bbox_inches='tight')
    plt.close()


def normalize_values(vector):
    maxval = 50
    for val in vector:
        if val < 50:
            maxval = val
            break
    for i in range(len(vector)):
        if vector[i] > 50:
            vector[i] = maxval
    return vector

def plot_distribution(vector, label, fname, color='-b', mode=None):
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    if mode:
        vector = normalize_values(vector)

    ax.plot(range(len(vector)), vector, color)
    plt.xlabel('Tempo')
    plt.ylabel(label)
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    plt.savefig(fname, bbox_inches='tight')
    plt.close()


def main_plot(bagname):
    bagname = fh.is_file(bagname)
    fname, ext = fh.filename(bagname)
    if ext == '.bag':
        dirout = fh.mkdir_from_file(bagname)
        fileinput = join(dirout, fname+'.pkl')
    elif ext == '.pkl':
        dirout = dirname(bagname)
        fileinput = bagname
    else:
        logger.error('File {} is not pickle or bag'.format(bagname))
        sys.exit()
    fileinput = fh.is_file(fileinput)
    logger.info('Reading file: %s' % fileinput)
    with open(fileinput, 'rb') as f:
        dic = pickle.load(f)

    fplot = join(dirout, fname+'_trajectory.pdf')
    logger.info('Saving plot: {}'.format(fplot))
    plot_trajectories(dic['boat1'], dic['boat2'], fplot, angle1=120, angle2=30)
    
    fplot = join(dirout, fname+'_dcpa.pdf')
    logger.info('Saving plot: {}'.format(fplot))
    plot_distribution(dic['stats'].dic['dcpa'], 'Valor de DCPA', fplot, color='tab:blue') 

    fplot = join(dirout, fname+'_tcpa.pdf')
    logger.info('Saving plot: {}'.format(fplot))
    plot_distribution(dic['stats'].dic['tcpa'], 'Valor de TCPA', fplot, color='tab:orange') 

    fplot = join(dirout, fname+'_distance.pdf')
    logger.info('Saving plot: {}'.format(fplot))
    plot_distribution(dic['stats'].dic['distance'], 'Distancia em metros', fplot, color='tab:green', mode=True) 

    fplot = join(dirout, fname+'_computation.pdf')
    logger.info('Saving plot: {}'.format(fplot))
    plot_distribution(dic['stats'].dic['computation'], 'Custo computacional', fplot, color='tab:red') 
    
        #os.remove(fileinput)
  

def main(bagfolder):
    fhandler = fh.FolderHandler(bagfolder, ext='bag')
    for bagname in fhandler:
        main_plot(bagname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='input_file', help='Folder containing bags or pickle file')
    args = parser.parse_args()
    if isdir(args.input):
        main(args.input)
    elif isfile(args.input):
        main_plot(args.input)
    else:
        logger.error('{} is not a pickle file or folder containing bag file'.format(args.input))

#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import os
from os.path import join, isdir
import tarfile

PATH = '/usr/share/datasets/Trainman/Kitchen/Model/'

def genStructure(rootname, net):
    """
    Create the structure to a new experiment. The structure is as follows:
        ROOT [/usr/share/datasets/Trainman/Kitchen/Model/]
         |-- Net [AlexNet]
              |-- Experiment [exp10_160614]
                    |-- Proto
                    |     |-- deploy.prototxt
                    |     |-- readme.md
                    |     |-- solver.prototxt
                    |     |-- train_val.prototxt
                    |-- Results
                    |-- Snapshots

    Parameters:
    -----------
    rootname : string
        name of the experiment e.g. `exp10_160614`
    net : string
        name of the net e.g. `AlexNet`
    """
    # extract content
    efolder = join(PATH, net, rootname)
    if not isdir(efolder):
        os.mkdir(efolder)
    with tarfile.open("structure/default_alexnet.tar.gz") as tar:
        tar.extractall(efolder)

    path_train = join(efolder, 'Proto', 'path_train.txt')
    path_val = join(efolder, 'Proto', 'path_val.txt')
    path_test = join(efolder, 'Proto', 'path_test.txt')

    # change train_val.prototxt
    doc = ''.join(open(join(efolder, 'Proto', 'train_val.prototxt')).readlines())
    doc = doc.replace('<SOURCE>', path_train)
    doc = doc.replace('<SOURCE_VAL>', path_val)
    doc = doc.replace('<SOURCE_TEST>', path_test)
    fout = open(join(efolder, 'Proto', 'train_val.prototxt'), 'w')
    fout.write(doc)
    fout.close()

    # change solver.prototxt
    doc = ''.join(open(join(efolder, 'Proto', 'solver.prototxt')).readlines())
    path_source = join(efolder, 'Proto', 'train_val.prototxt')
    path_snap = join(efolder, 'Snapshots/')
    doc = doc.replace('<TRAIN_PROTO>', path_source)
    doc = doc.replace('<SNAPSHOTS>', path_snap)
    fout = open(join(efolder, 'Proto', 'solver.prototxt'), 'w')
    fout.write(doc)
    fout.close()

    # set permissions
    for (dirpath, dirnames, filenames) in os.walk(efolder):
        os.chmod(dirpath, 0770)
        for dirn in dirnames:
            os.chmod(join(dirpath, dirn), 0770)
        for f in filenames:
            os.chmod(join(dirpath, f), 0770)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', metavar='folder_experiment', help='folder name to the experiment')
    parser.add_argument('-n', '--net', metavar='net', help='name of the net', default='AlexNet')
    args = parser.parse_args()

    genStructure(args.experiment, args.net)

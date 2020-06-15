#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import linecache
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import ast
import numpy as np
from os.path import realpath, dirname, splitext, exists
from os.path import basename, isfile, isdir, join

import progressbar

class Stats(object):
    def __init__(self, name):
        self.name = name
        self.dic = {}

    def add(self, key, value):
        if key not in self.dic:
            self.dic[key] = [value]
        else:
            self.dic[key].append(value)

    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self.dic, f)
#End class Stats


class Boat(object):
    def __init__(self, name):
        self.name = name
        self.x = []
        self.y = []
    
    def add_x(self, value):
        self.x.append(value)

    def add_y(self, value):
        self.y.append(value)
#End class Boat

class FolderHandler(object):
    """ Class to deal with folders """
    def __init__(self, inputfolder, ext='txt', sort_id=False):
        self.inputfolder = inputfolder
        self.ext = ext
        self.sort_id = sort_id
        self.id = -1
        self.dfiles = {}
        self.files = []
        self.exist_folder()
        self._load_paths()

    def __iter__(self):
        if self.sort_id:
            for id in sorted(self.dfiles):
                self.id = id
                yield self.dfiles[id]
        else:
            for path in sorted(self.files):
                yield path

    def _load_paths(self):
        for root, dirs, files in os.walk(self.inputfolder, topdown=False):
            for name in files:
                fname, ext = splitext(name)
                if ext[1:] == self.ext:
                    path = join(root, name)
                    if self.sort_id:
                        self.dfiles[int(fname)] = path
                    else:
                        self.files.append(path)
        return self

    def exist_folder(self):
        if not exists(self.inputfolder):
            logger.error('{} is not a valid folder'.format(self.inputfile))
            sys.error()
        return

    def nb_files(self):
        if self.sort_id:
            return len(self.dfiles)
        return len(self.files)
# End of FileHandler class

def is_file(inputfile):
    """ Check whether the ``inputfile`` corresponds to a file """
    inputfile = realpath(inputfile)
    if not isfile(inputfile):
        logger.error('Input is not a file!')
        sys.exit(0)
    return inputfile


def is_folder(inputfolder):
    """ Check whether the ``inputfolder`` corresponds to a folder """
    inputfolder = realpath(inputfolder)
    if not isdir(inputfolder):
        logger.error('Argument %s is not a folder!' % inputfolder)
        sys.exit(0)
    return inputfolder


def filename(path, extension=True, string=False):
    fname, ext = splitext(basename(path))
    if string:
        return '%s%s' % (fname, ext)
    if extension:
        return fname, ext
    return fname


def add2dic(dic, key, value):
    if dic.has_key(key):
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic


def mkdir_from_file(path):
    """ Create a folder with the same name of the file (without extension)"""
    path = realpath(path)
    dirfile = dirname(path)
    fname, ext = filename(path)
    dirout = join(dirfile, fname)
    if exists(dirout):
        logger.warning('Folder %s already exists!' % dirout)
    else:
        os.makedirs(dirout)
    return dirout


def sort_by_name(list_images):
    """ sort images by name """
    ids = []
    for name in list_images:
        fname, ext = splitext(basename(name))
        ids.append(int(fname))
    list_names = [str(name)+'.jpg' for name in sorted(ids)]
    return list_names


def create_paths(inputfolder, fileoutput, path=None):
    fout = open(fileoutput, 'w')

    files = os.listdir(inputfolder)
    names = []
    for img in files:
        name, ext = splitext(img)
        if ext == '.jpg':
            names.append(int(name))
    for name in sorted(names):
        if path:
            fout.write('%s/%d.jpg\n' % (path, name))
        else:
            fout.write('%s/%d.jpg\n' % (inputfolder, name))
    logger.info('Saved paths in file: %s' % fileoutput)


class PathfileHandler(object):
    """Class to deal with files containing paths and labels/features"""

    def __init__(self, inputfile, display=True, load=False, sep=' '):
        """Initializes the class
        
        Parameters
        ----------
        inputfile : string
            path to the file containing images and labels/features
        display : boolean
            show the progress bar
        load : boolean
            load path, labels and feats vectors in case they exist
        """
        self.display = display
        self.inputfile = realpath(inputfile)
        self.inputdir = dirname(inputfile)
        self.nb_lines = self.count_lines(inputfile)
        self.sep = sep
        self.path = None
        self.feats = None

        if load:
            self.vpaths, self.vfeats = load_file(inputfile)


    def __iter__(self):
        """Iterates the file yielding the path, the true label and a vector of 
        features when exists
        """
        pb = progressbar.ProgressBar(self.nb_lines)
        with open(self.inputfile) as fin:
            for line in fin:
                arr = line.strip().split(self.sep)
                if arr:
                    self.path = arr[0]
                    if len(arr) == 2 and arr[1]:
                        self.feats = arr[1]
                        yield self.path, self.feats
                    elif len(arr) > 1 and arr[1]:
                        self.feats = arr[1:]
                        yield self.path, self.feats
                    else:
                        yield self.path
                if self.display:
                    pb.update()


    @staticmethod
    def load_file(inputfile):
        """ Load the content of pathfile into `path`, `label` and `feats`
        """
        logger.debug('Loading file: %s' % inputfile)
        vpaths, vfeats = [], []
        with open(inputfile) as fin:
            for line in fin:
                arr = line.strip().split()
                if arr:
                    vpaths.append(arr[0])
                elif len(arr) > 1:
                    vfeats.append(arr[2:])
        return vpaths, vfeats


    @staticmethod
    def count_lines(inputfile):
        """ Returns the total number of images in the input file 

        Parameters
        ----------
        inputfile : string
            path to the file containing images and labels/features

        Returns
        -------
        n : int
            total number of lines in the document
        """
        with open(inputfile) as fin:
            for n, _ in enumerate(fin, start=1): pass
        return n


    def header(self):
        """ Return the first line of the file """
        with open(self.inputfile) as fin:
            h = fin.next().strip()
        return h


    def get_line(self, nb_line):
        """Returns the line at number `nb_line`"""
        return linecache.getline(self.inputfile, nb_line).strip()


    def get_path(self, nb_line, label=False):
        """Returns the path of the line at number `nb_line`"""
        line = linecache.getline(self.inputfile, nb_line)
        path = None
        if line:
            arr = line.split()
            path = arr[0]
            if label:
                y = arr[1]
                return path, y
        return path


    def features_line(self, nb_line, asstr=False):
        """Returns only the feature of the line number `nb_line`"""
        line = linecache.getline(self.inputfile, nb_line)
        arr = line.strip().split()
        if len(arr) > 2:
            if asstr:
                return ' '.join(arr[2:])
            else:
                return arr[2:]
        return None


    def current_features(self, N=2):
        """
        Return a list containing the `N` features with the highest scores

        Parameters:
        -----------
        N : int
            number of features to return

        Notes:
        ------
        The output has the form of a list as:
        [(1, 0.33), (3, 0.12), (5, 0.08), ...]
        """
        features = self.labels[1:]
        classes = map(int, features[0::2])
        preds = np.array(features[1::2], dtype=np.float32)
        topN = []
        for n in range(N):
            valmax = preds.max()
            imax = preds.argmax()
            topN.append((classes[imax], valmax))
            preds[imax] = -1
        return topN


    def has_features(self):
        """
        Returns
        -------
        _ : bool
            False : only path and label
            True : path, label and features
        """
        line = self.get_line(1)
        arr = line.strip().split()
        if len(arr) > 2:
            return True
        else:
            return False
#End of class PathfileHandler

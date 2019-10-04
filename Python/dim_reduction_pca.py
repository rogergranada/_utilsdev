#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, chi2
from os.path import realpath, join, basename, splitext, dirname


def load_dataframe(input):
    """ Load input file as a dataframe """ 
    with(open(input)) as fin: 
        nbcols = len(fin.readline().strip().split())
    init_cols = ['path', 'label']
    feat_cols = [ 'ft'+str(i) for i in range(nbcols-2) ]
    output = pd.read_csv(input, sep=' ', header=None)
    output.columns = init_cols + feat_cols + ['None']
    return output, feat_cols


def name_output(input, nbfeats, comp=None):
    """ Generate a name to the output file based on the input file """
    dname = dirname(input)
    fname, ext = splitext(basename(input))
    if comp:
        return join(dname, fname+str(nbfeats)+'_'+comp+ext)
    return join(dname, fname+str(nbfeats)+ext)


def apply_PCA(ftrain, fval, ftest, nb_components, explain_variance=False):
    """ Performs feature selection using PCA from sklearn """
    pca = PCA(n_components=nb_components, svd_solver='full', random_state=1001)
    for i, input in enumerate([ftrain, fval, ftest]):
        logger.info('Processing %s' % input)
        fout = open(name_output(input, nb_components, comp='pca'), 'w')
        df, feat_cols = load_dataframe(input)
        if i == 0:
            pca.fit(df[feat_cols].values)
        vfeats = pca.transform(df[feat_cols].values)
        for p, l, feats in zip(df['path'].values, df['label'].values, vfeats):
            feats = ' '.join(map(str, feats))
            fout.write('%s %d %s\n' % (p, l, feats))
    if explain_variance:
        explain = 0.0
        for j in range(nb_components):
            explain += pca.explained_variance_ratio_[j]
        logger.info('%d features explain %f of the data' % (nb_components, explain))


def feature_selection(ftrain, fval, ftest, nb_components):
    """ Performs feature selection using KBest from sklearn """
    kbest = SelectKBest(score_func=chi2, k=nb_components)
    for i, input in enumerate([ftrain, fval, ftest]):
        logger.info('Processing %s' % input)
        fout = open(name_output(input, nb_components, comp='kbest'), 'w')
        df, feat_cols = load_dataframe(input)

        if i == 0:
            fit = kbest.fit(df[feat_cols].values, df['label'].values)
        vfeats = kbest.transform(df[feat_cols].values)
        for p, l, feats in zip(df['path'].values, df['label'].values, vfeats):
            feats = ' '.join(map(str, feats))
            fout.write('%s %d %s\n' % (p, l, feats))


def main(ftrain, fval, ftest, algorithm, nb_dim):
    ftrain = realpath(ftrain)
    fval = realpath(fval)
    ftest = realpath(ftest)
    if algorithm == 'pca':
        apply_PCA(ftrain, fval, ftest, nb_dim)
    elif algorithm == 'kbest':
        feature_selection(ftrain, fval, ftest, nb_dim)
    else:
        logger.error('Algorithm "%s" not implemented' % algorithm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('train', metavar='file_train', help='File containing training features.')
    parser.add_argument('validation', metavar='file_val', help='File containing validation features.')
    parser.add_argument('test', metavar='file_test', help='File containing test features.')
    parser.add_argument('algorithm', metavar='algorithm', help='Algorithm to perform dimension reduction (pca|kbest).')
    parser.add_argument('-d', '--dimension', default=1024, type=int, help='Number of dimensions in the output.')
    args = parser.parse_args()
    main(args.train, args.validation, args.test, args.algorithm, args.dimension)

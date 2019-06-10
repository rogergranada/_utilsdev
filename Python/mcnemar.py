#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
From two files containing the following structure:

<filepath> <true_label> <predicted_label>

Calculate the McNemar's statistical test, returning the p-value for
statistical significance.

Contingence table is created as:

        | model_2  | model_2 |
        | correct  | wrong   |
        |----------|---------|
model_1 |          |         |
correct |    a     |    b    |
        |----------|---------|      
model_1 |    c     |    d    |
wrong   |          |         |
"""
import sys
import argparse
import logging
import numpy as np
from mlxtend.evaluate import mcnemar_table
from mlxtend.evaluate import mcnemar
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main(file_1, file_2):
    a, b, c, d = 0, 0, 0, 0
    nb_lines = 0
    y_ground, y_1, y_2 = [], [], []
    with open(file_1) as f1, open(file_2) as f2:
        for line_1, line_2 in zip(f1, f2):
            ground_1, pred_1 = map(int, line_1.strip().split()[1:])
            ground_2, pred_2 = map(int, line_2.strip().split()[1:])
            if ground_1 != ground_2:
                logger.error('Files do not belong to the same dataset')
                sys.exit(1)

            y_ground.append(ground_1)
            y_1.append(pred_1)
            y_2.append(pred_2)
            if pred_1 == ground_1:
                if pred_2 == ground_1:
                    a += 1
                else:
                    b += 1
            else:
                if pred_2 == ground_1:
                    c += 1
                else:
                    d += 1
            nb_lines += 1
    logger.info('Loaded {} lines..'.format(nb_lines))
    logger.info('| {} | {} |'.format(a, b))
    logger.info('| {} | {} |'.format(c, d))

    y_ground = np.array(y_ground)
    y_1 = np.array(y_1)
    y_2 = np.array(y_2)

    tb = mcnemar_table(y_target=y_ground, 
                   y_model1=y_1, 
                   y_model2=y_2)
    logger.info('\n {}'.format(tb))

    chi2, p = mcnemar(ary=tb, corrected=True)
    logger.info('chi-squared: {}'.format(chi2))
    logger.info('p-value: {}'.format(p))
        
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_1", help="Path to the file containing the results for model 1.")
    parser.add_argument("file_2", help="Path to the file containing the results for model 2.")
    args = parser.parse_args()

    main(args.file_1, args.file_2)



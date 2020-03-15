#!/usr/bin/env python
# coding: utf-8
"""
This script simulates `The Wall` game, where there is a wall containing 
seven slots to place a ball. The ball will fall the wall knocking a series 
of pins that may deviate the ball to one of the fifteen slots in the bottom.

In this script the user can simulate a series of balls into a single position
and check the distribution of the bottom slots, or describe the distribution
for all positions using series of balls. 
"""
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import sys
import argparse
import random
from matplotlib import pyplot as plt
import numpy as np

def run_wall(position, places, scores, degrees):
    """  Roll the ball from `position` down to the score """    
    center = ((scores - places)/2) 
    min_score = center - places
    max_score = center + places
    for i in range(degrees):
        side = random.choice([True, False])
        if i % 2 == 0:
            if side:
                if position == max_score:
                    possible = [position-1, position]
                else:
                    possible = [position, position+1]
            else:
                if position == min_score:
                    possible = [position, position+1]
                else:
                    possible = [position-1, position]
        else:
            if side:
                position = possible[1]
            else:
                position = possible[0]
        #print side, position
    position -= min_score
    return position


def run_many(places, degrees, scores, nb_runs=1):
    fig, ax = plt.subplots()
    labels = [str(i+1) for i in range(scores)] 
    x = np.arange(len(labels))  # the label locations
    widths = [-0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9]

    bars = []
    for position in range(1, places+1):
        print 'Place to set the ball: ', position
        sequence = [0]*scores
        for run in range(nb_runs):
            score = run_wall(position, places, scores, degrees)
            sequence[score] += 1
        rel = ax.bar(x+widths[position-1], sequence, width=0.2, label=labels[i])
        bars.append(rel[0])
    ax.legend(bars, labels)
    plt.show()


def run_single(position, places, degrees, scores, nb_runs=1):
    labels = [str(i) for i in range(scores)] 
    print 'Place to set the ball: ', position
    sequence = [0]*scores
    for run in range(nb_runs):
        score = run_wall(position, places, scores, degrees)
        sequence[score] += 1
    plt.bar(labels, sequence)
    plt.show()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', metavar='position', help='Number to try the wall', type=int)
    parser.add_argument('-p', '--places', help='Number of places in the top of the wall', type=int, default=7)
    parser.add_argument('-d', '--degrees', help='Number of degrees (pins) from top to down', type=int, default=12)
    parser.add_argument('-s', '--scores', help='Number of scores in the bottom of the wall', type=int, default=15)
    parser.add_argument('-r', '--runs', help='Number of runs to try the wall', type=int, default=10000)
    args = parser.parse_args()
    
    if args.places <= 0 or args.degrees <= 0 or args.scores <= 0 or args.runs <= 0:
        logger.error("Invalid number of places, degrees or scores.")
        sys.exit(0)
    if args.position <= 0 or args.position > args.places:
            logger.error("Invalid position!")
            sys.exit(0)    

    #run_single(args.position, places=args.places, degrees=args.degrees, scores=args.scores, nb_runs=args.runs)
    run_many(args.places, args.degrees, args.scores, args.runs)

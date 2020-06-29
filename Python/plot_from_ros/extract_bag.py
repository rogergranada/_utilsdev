#/usr/bin/env python

"""
Set variables in .bashrc before running

# ROS
export ROS_ROOT=/opt/ros/kinetic
export ROS_DISTRO=kinetic
export ROS_PACKAGE_PATH=/opt/ros/kinetic/share
export PATH=$PATH:/opt/ros/kinetic/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/ros/kinetic/lib
export PYTHONPATH=/opt/ros/kinetic/lib/python2.7/site-packages
export ROS_MASTER_URI=http://localhost:11311
export CMAKE_PREFIX_PATH=/opt/ros/kinetic
source $ROS_ROOT/setup.bash
"""

import os
import argparse
import sys
import rosbag
import numpy as np
from os.path import exists, dirname, join

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pickle
import numpy as np

import filehandler as fh
from filehandler import Stats, Boat

TOPICS = ['diffboat1/state', 
          '/diffboat2/state', 
          '/diffboat1/move_base/RRAPlannerROS/d_cpa', 
          '/diffboat1/cmd_vel', 
          '/diffboat1/move_base/RRAPlannerROS/computation_time', 
          '/diffboat1/move_base/RRAPlannerROS/distance', 
          '/diffboat1/move_base/RRAPlannerROS/t_cpa'
]


def print_topic_info(bag):
    """ Print topic, messages and frequency """
    dtopics = bag.get_type_and_topic_info()[1]
    for tpc in dtopics:
        vals = dtopics[tpc]
        logger.info('Topic: {}'.format(tpc))
        logger.info('- Count: {}'.format(vals[1]))
        logger.info('- Frequency: {}'.format(vals[3])) 


def main_extract(bagname):
    bagname = fh.is_file(bagname)
    fname, ext = fh.filename(bagname)
    if ext == '.bag':
        dirout = fh.mkdir_from_file(bagname)
        logger.info('Reading bag %s' % bagname)
        bag = rosbag.Bag(bagname)
        boat1 = Boat('Boat 1')
        boat2 = Boat('Boat 2')
        sim = Stats(fname)

        dtopics = bag.get_type_and_topic_info()[1]
        bag_messages = bag.read_messages()
        for topic, msg, timestamp in bag_messages:
            if topic == 'diffboat1/state':
                boat1.add_x(msg.pose.pose.position.x)
                boat1.add_y(msg.pose.pose.position.y)
            elif topic == '/diffboat2/state':
                boat2.add_x(msg.pose.pose.position.x)
                boat2.add_y(msg.pose.pose.position.y)
            elif topic == '/diffboat1/move_base/RRAPlannerROS/d_cpa': 
                sim.add('dcpa', msg.data)
            elif topic == '/diffboat1/move_base/RRAPlannerROS/t_cpa':
                sim.add('tcpa', msg.data)
            elif topic == '/diffboat1/move_base/RRAPlannerROS/distance':
                sim.add('distance', msg.data)
            elif topic == '/diffboat1/move_base/RRAPlannerROS/computation_time':
                sim.add('computation', msg.data)
        
        fout = join(dirout, fname+'.pkl')
        logger.info('Saving file: {}'.format(fout))
        d = {'boat1': boat1, 'boat2': boat2, 'stats': sim}
        with open(fout, 'wb') as f:
           pickle.dump(d, f)


def main(bagfolder):
    fhandler = fh.FolderHandler(bagfolder, ext='bag')
    for bagname in fhandler:
        main_extract(bagname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('bagfile', metavar='bag_file', help='Bag or folder containing several bags')
    args = parser.parse_args()
    if fh.is_folder(args.bagfile):
        main(args.bagfile)
    elif fh.is_file(args.bagfile):
        main_extract(args.bagfile)
    else:
        logger.info('Path does not contain bag files')
    

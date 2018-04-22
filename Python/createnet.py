#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
from os.path import join, isdir
import graphviz as gv
import re


class ParseProto(object):
    """
    Parse the prototxt file
    """
    def __init__(self, fname):
        """
        Initiate class ParseProto.
        
        Parameters:
        -----------
        fname : string
            path to the prototxt file containing the network structure
        """
        self.fname = fname
        self.netname = None

    def _getElement(self, line):
        el = re.findall(r'"\w+"', line)[0]
        return el.replace('"', '')


    def __iter__(self):
        """
        Iterates over the file extracting:
            name, type, bottom, top
        from each layer.
        """
        outLayer = False
        with open(self.fname) as fin:
            for line in fin:
                line = line.strip()

                # name of the network
                if not self.netname and line.startswith('name'):
                    name = re.findall(r'"\w+"', line)[0]
                    self.netname = name.replace('"', '')

                # begining of each layer
                elif line.startswith('layer'):
                    if outLayer:
                        yield name, typed, lbot, ltop
                        
                    ltop, lbot = [], []
                    name, typed = '', ''
                    outLayer = True
                elif not line.startswith('#'):
                    if line.startswith('name:'):
                        name = self._getElement(line)
                    if line.startswith('type:'):
                        typed = self._getElement(line)
                    elif line.startswith('bottom:'):
                        lbot.append(self._getElement(line))
                    elif line.startswith('top:'):
                        ltop.append(self._getElement(line))

        
                

def applyStyles(gr):
    styles = {
        'graph': {
            'label': 'A Fancy Graph',
            'fontsize': '16',
            'fontcolor': 'white',
            'bgcolor': '#333333',
            'rankdir': 'BT'
        },
        'nodes': {
            'fontname': 'Helvetica',
            'shape': 'hexagon',
            'fontcolor': 'white',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#006699'
        },
        'edges': {
            'style': 'dashed',
            'color': 'white',
            'arrowhead': 'open',
            'fontname': 'Courier',
            'fontsize': '12',
            'fontcolor': 'white'
        }
    }
    gr.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    gr.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    gr.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    gr.render('g6')
    return gr

def generateImage(fnet):
    """
    Create the image of the net using Graphviz.
    
    Parameters:
    -----------
    fnet : string
        path to the train_val file containing the net structure
    """
    proto = ParseProto(fnet)
    imgv = gv.Digraph(format='svg')
    layer = {}
    for name, typed, lbot, ltop in proto:
        print name, typed, lbot, ltop
    #    layer[name] = {'type': typed, 'bottom': lbot, 'top': ltop}

    # build nodes as layers
    for name in layer:
        imgv.node(name)

    # connect edges
    for name in layer:
        for bottom in layer[name]['bottom']:
            if bottom != name:
                imgv.edge(bottom, name)
        for top in layer[name]['top']:
            if top != name:
             imgv.edge(name, top)
    #applyStyles(imgv)
    #imgv.render('graph')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('netfile', metavar='file_net', help='file containing the structure of the network')
    #parser.add_argument('-n', '--net', metavar='net', help='name of the net', default='AlexNet')
    args = parser.parse_args()

    generateImage(args.netfile)

#!/bin/bash

HOME="/usr/share/datasets/Trainman/Kitchen/Data/"
ACTIONS="boild-egg ham-egg kinshi-egg omelette scramble-egg"
#DATA="data1 data2 data3 data4 data5 data6 data7"
DATA="data7"
IMAGES="bg256"
#IMAGES="bg256 img256"

for data in $DATA; do
    for activity in $ACTIONS; do
        for img in $IMAGES; do
            echo 'Copying '$HOME/$data/$activity/$img
            #mkdir -p $data/$activity/$img
            scp user@server:$HOME/$data/$activity/$img/* $data/$activity/$img 
        done
    done
done

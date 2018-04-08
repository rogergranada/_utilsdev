#!/bin/bash

CONTADOR=1
PHOTO_FOLDER="/home/roger/Desktop/europarl-v7pt/"

#In photo folder type:
#$rename 's/ /_/g' *

for ARQ_FOTO in `ls $PHOTO_FOLDER`; do
    if [ ${CONTADOR} -lt '10' ]; then
        mv $PHOTO_FOLDER"/$ARQ_FOTO" $PHOTO_FOLDER"/europarl-v7.pt0$CONTADOR.txt"
    else
        mv $PHOTO_FOLDER"/$ARQ_FOTO" $PHOTO_FOLDER"/europarl-v7.pt$CONTADOR.txt"
    fi
    CONTADOR=`expr $CONTADOR + 1`
done



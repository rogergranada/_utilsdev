#!/bin/bash

CONTADOR=1
PHOTO_FOLDER="/media/Diversos/20140726/"

#In photo folder type:
#$rename 's/ /_/g' *

for ARQ_FOTO in `ls $PHOTO_FOLDER`; do
    mogrify -resize 1024 -quality 85 $PHOTO_FOLDER"/$ARQ_FOTO"
done



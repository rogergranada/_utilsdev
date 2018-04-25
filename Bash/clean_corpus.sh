#!/bin/sh

INPUT=$1
OUTPUT="/home/roger/Programs/Output/"

if [ $# -ne 1 ]; then
	echo "error!\ntry: ./clean_corpus.sh <input folder>"
else
	if [ -d $OUTPUT ]; then
		rm -rf ${OUTPUT}*
	else
		mkdir $OUTPUT
	fi	

	ls $INPUT | while read fileinput; do  
		if [ -f $INPUT"$fileinput" ]; then
			cat $INPUT"$fileinput" | tr "[:upper:]" "[:lower:]" | tr '!.;:,?()[]{}"@#$%&*_+=\/<>-' ' ' > ${OUTPUT}"$fileinput"
		fi
	done
fi

#!/bin/sh

INPUT=$1
OUTPUT=/home/roger/Programs/Output

BIN=/home/roger/Programs/LinguaToolkit/MultiLingua/tree-tagger/bin
CMD=/home/roger/Programs/LinguaToolkit/MultiLingua/tree-tagger/cmd
LIB=/home/roger/Programs/LinguaToolkit/MultiLingua/tree-tagger/lib
TOKENIZER=$BIN/separate-punctuation
TAGGER=$BIN/tree-tagger
ABBR_LIST=$LIB/english-abbreviations
PARFILE=$LIB/english.par

ls $INPUT | while read FILEINPUT; do
	echo "Tagging $FILEINPUT"
	
	#TreeTagger files
	cat $INPUT/$FILEINPUT |
	$TOKENIZER +1 +s +l $ABBR_LIST |
	sed -e "s/'s"'$'"/ 's/g" \
	-e "s/s'"'$'"/ '/g" \
	-e "s/n't"'$'"/ n't/g" \
	-e "s/'re"'$'"/ 're/g" \
	-e "s/'ve"'$'"/ 've/g" \
	-e "s/'d"'$'"/ 'd/g" \
	-e "s/'m"'$'"/ 'm/g" \
	-e "s/'em"'$'"/ 'em/g" \
	-e "s/'ll"'$'"/ 'll/g" \
	-e '/^$/d' |
	tr ' ' '\n' |
	grep -v '^$' |
	$TAGGER $PARFILE -token -lemma -sgml > $OUTPUT/"$FILEINPUT"
	
done



#!/bin/bash
SEARCH_PATTERN=$1
OUTPUT=$2
grep -o "$SEARCH_PATTERN" mobydick.txt > temp.txt
OCCURRENCES=$(cat temp.txt | wc -l)
echo "The search pattern $SEARCH_PATTERN was found $OCCURRENCES times" > $OUTPUT

#!/bin/bash

# Input file: mock_data.tsv
# Command: tr '\t' ',' < file.tsv > file.csv
# tr command = translate/convert

if [ -z "$1" ]; then
   echo "This script converts a TSV into a CSV"
   echo "usage: detabify.sh <input.tsv> <output.csv>"
   exit 1;
fi

tr '\t' ',' < $1 > $2 || exit 99;
echo "Conversion complete! $1 -> $2"
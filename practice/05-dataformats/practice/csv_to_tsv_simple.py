#!/usr/bin/env python3
import sys

# get input and output filenames from command line args
if len(sys.argv) != 3:
	print("Usage: python3 csv_to_tsv_simply.py <input.csv> <output.tsv>")
	sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# read csv file as text and convert to tsv
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
	for line in infile:
		# replace commas with tabs
		tsv_line = line.replace(',', '\t')
		outfile.write(tsv_line)


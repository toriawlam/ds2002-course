#!/usr/bin/env python
import sys
import pandas as pd

# get input and output filenames from command line arguments
if len(sys.argv) != 3:
	print("Usage: python3 csv_to_tsv_pandas.py <input.csv> <output.tsv>")
	sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# read csv file
df = pd.read_csv(input_file)

# write as tsv
df.to_csv(output_file, sep='\t', index=False)

print(f"Conversion complete! {input_file} -> {output_file}")

#!/usr/bin/env python
import pandas as pd
import sys
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Get input and output filenames from command line arguments
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        logging.error(f"Usage: python {sys.argv[0]} <input.csv> <output.tsv>")
        sys.exit(1)

    # Read CSV file
    df = pd.read_csv(input_file)

    # Write as TSV (tab-separated)
    df.to_csv(output_file, sep='\t', index=False)

    logging.info(f"Conversion complete! {input_file} -> {output_file}")

if __name__ == "__main__":
    main()
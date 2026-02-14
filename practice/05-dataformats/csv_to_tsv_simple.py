#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        logging.error(f"Usage: python {sys.argv[0]} <input.csv> <output.tsv>")
        sys.exit(1)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Replace commas with tabs
            tsv_line = line.replace(',', '\t')
            outfile.write(tsv_line)

    logging.info(f"Conversion complete! {input_file} -> {output_file}")

if __name__ == "__main__":
    main()
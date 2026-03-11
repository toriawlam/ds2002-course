#!/usr/bin/env python3

"""
Process a text file and count the number of words.
Usage: python process-text.py <input_file> <output_file>
"""

import sys

def parse_args():
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print("Usage: python process-text.py <input_file> <output_file>")
        sys.exit(1)
    return input_file, output_file

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
    words = text.split()
    return len(words)

def save_result(input_file, num_words, output_file):
    with open(output_file, 'w') as f:
        f.write(f"Input file: {input_file}\n")
        f.write(f"Number of words: {num_words}\n")

def main():
    input_file, output_file = parse_args()
    print(f"Processing {input_file}")
    num_words = process_file(input_file, output_file)
    save_result(input_file, num_words, output_file)
    print(f"Saved result to {output_file}")

if __name__ == "__main__":
    main()
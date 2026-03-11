#!/bin/bash
# Create book-1.txt through book-5.txt for the job array text-processing example.
# Run from your job working directory (e.g. /scratch/$USER/ds2002-jobruns) or pass a path.

WORKDIR="${1:-.}"
if [ ! -d $WORKDIR ]; then
    mkdir -p $WORKDIR
fi
cd "$WORKDIR"

# create 5 book files
# Pride and Prejudice by Jane Austen
curl -s https://www.gutenberg.org/files/1342/1342-0.txt > book-1.txt
# Count of Monte Cristo by Alexandre Dumas
curl -s https://www.gutenberg.org/files/1184/1184-0.txt > book-2.txt
# White Fang by Jack London
curl -s https://www.gutenberg.org/files/910/910-0.txt > book-3.txt
# Dracula by Bram Stoker
curl -s https://www.gutenberg.org/files/45839/45839-0.txt > book-4.txt
# Metamorphosis by Franz Kafka
curl -s https://www.gutenberg.org/files/5200/5200-0.txt > book-5.txt

echo "Created book-1.txt through book-5.txt in $WORKDIR"

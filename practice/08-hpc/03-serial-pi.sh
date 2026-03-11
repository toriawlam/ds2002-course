#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=pi
#SBATCH --output=pi-serial-%j.out
#SBATCH --error=pi-serial-%j.err
#SBATCH --time=00:01:00
#SBATCH --partition=standard
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

NUM_POINTS=100000000
OUTPUT_FILE=pi.csv

python ~/ds2002-course/practice/08-hpc/serial-pi.py $NUM_POINTS $OUTPUT_FILE
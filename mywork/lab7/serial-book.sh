#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=lab7
#SBATCH --output=serial-book-%j.out
#SBATCH --error=serial-book-%j.err
#SBATCH --time=00:10:00
#SBATCH --partition=standard
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

WORKDIR=/scratch/$USER/ds2002-jobruns/text-analysis
cd "$WORKDIR"

python ~/ds2002-course/labs/07-hpc/process-book.py book-1.txt results-1.csv
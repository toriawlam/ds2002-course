#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=text-array
#SBATCH --output=text-array-%A_%a.out
#SBATCH --error=text-array-%A_%a.err
#SBATCH --partition=standard
#SBATCH --time=00:05:00
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --array=1-5

# One input/output pair per array task (data-1.txt -> results-1.txt, etc.)
INPUT="data-${SLURM_ARRAY_TASK_ID}.txt"
OUTPUT="results-${SLURM_ARRAY_TASK_ID}.txt"

module load miniforge
source activate ds2002
# Assumed that you cloned the repo to ~/ds2002-course. 
python ~/ds2002-course/practice/08-hpc/process-text.py "$INPUT" "$OUTPUT"

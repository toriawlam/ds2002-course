#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=pi
#SBATCH --output=pi-mp-%j.out
#SBATCH --error=pi-mp-%j.err
#SBATCH --time=00:01:00
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=8G            # for each cpu core; total memory 8 * 8GB = 64GB
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8          # for multiprocessing

NUM_POINTS=100000000
OUTPUT_FILE=pi.csv

# use $SLURM_CPUS_PER_TASK to get the number of CPU cores assigned to the job
# use $SLURM_MEM_PER_CPU to get the amount of memory assigned to each CPU core
echo "Number of CPU cores assigned to the job: $SLURM_CPUS_PER_TASK"
echo "Amount of memory assigned to each CPU core: $SLURM_MEM_PER_CPU"

# we pass the number of CPU cores assigned to the job to set up the ideal number of processes inside the python script
python ~/ds2002-course/practice/08-hpc/mp-pi.py $NUM_POINTS $OUTPUT_FILE $SLURM_CPUS_PER_TASK
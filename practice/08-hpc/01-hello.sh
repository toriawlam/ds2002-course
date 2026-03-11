#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=hello
#SBATCH --output=hello-%j.out
#SBATCH --error=hello-%j.err
#SBATCH --time=00:01:00             # 1 minute
#SBATCH --partition=standard
#SBATCH --mem=8G
#SBATCH --nodes=1                   # that's the default for standard partition
#SBATCH --ntasks-per-node=1         # that's the default for standard partition
#SBATCH --cpus-per-task=1           # that's the default for standard partition

# Execute some simple commands to print information about the job
# The output will be saved to the files specified in the #SBATCH --output and #SBATCH --error directives.
echo "Hello, ds2002!"
echo "The job is running on the $(hostname) node."
echo "The job id is $SLURM_JOB_ID"
echo "The job name is $SLURM_JOB_NAME."
echo "Available resources for this job:"
echo "  - CPU Cores (per task): $SLURM_CPUS_PER_TASK"
echo "  - Memory: $SLURM_MEM_PER_NODE"

# Redirect some output to a file
echo "Redirection of echo/print output to specific file" > hello.txt
# uncomment next line to print all environment variables related to SLURM
# printenv | grep SLURM >> hello.txt


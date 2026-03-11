#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=pytorch-example
#SBATCH --output=pytorch-%j.out
#SBATCH --error=pytorch-%j.err
#SBATCH --partition=gpu                 # needed to run on GPU device
#SBATCH --gres=gpu:1                    # needed to run on GPU device
#SBATCH --mem=32G
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00                 # 10 minutes

# get example Py script
curl -o pytorch-example.py https://raw.githubusercontent.com/pytorch/examples/refs/heads/main/mnist/main.py

# load environment
module load apptainer
module load pytorch

# run the example
apptainer run --nv $CONTAINERDIR/pytorch-2.9.0.sif pytorch-example.py
